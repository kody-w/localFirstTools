#!/usr/bin/env python3
"""
Apple Notes to Ghost Writer Sync Script
Extracts notes from Apple Notes and exports to JSON format compatible with Ghost Writer app
"""

import sqlite3
import os
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
import zlib
import struct

class AppleNotesExtractor:
    def __init__(self):
        self.notes_db_path = os.path.expanduser(
            "~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite"
        )
        self.notes_data = []
        
    def extract_notes_via_osascript(self):
        """
        Extract notes using AppleScript (more reliable method)
        """
        applescript = '''
        tell application "Notes"
            set notesList to {}
            repeat with eachNote in notes
                set noteRecord to {noteId:id of eachNote, noteTitle:name of eachNote, noteBody:body of eachNote, noteCreated:creation date of eachNote, noteModified:modification date of eachNote, noteFolder:name of container of eachNote}
                set end of notesList to noteRecord
            end repeat
            return notesList
        end tell
        '''
        
        try:
            # Run AppleScript
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Error running AppleScript: {result.stderr}")
                return []
            
            # Parse the AppleScript output
            notes = self._parse_applescript_output(result.stdout)
            return notes
            
        except Exception as e:
            print(f"Error extracting notes via AppleScript: {e}")
            return []
    
    def _parse_applescript_output(self, output):
        """
        Parse the AppleScript output into structured data
        """
        notes = []
        
        # The output is in AppleScript record format, we need to parse it
        # This is a simplified parser - you might need to adjust based on actual output
        note_pattern = r'noteId:([^,]+), noteTitle:([^,]+), noteBody:(.*?), noteCreated:([^,]+), noteModified:([^,]+), noteFolder:([^}]+)'
        
        # Split by record boundaries
        records = output.split('}, {')
        
        for record in records:
            # Clean up the record
            record = record.strip('{}')
            
            # Extract fields manually since AppleScript output can be complex
            try:
                # This is a more robust approach using subprocess with separate calls
                note_data = self._extract_single_note_data(record)
                if note_data:
                    notes.append(note_data)
            except Exception as e:
                print(f"Error parsing note record: {e}")
                continue
        
        return notes
    
    def extract_notes_individually(self):
        """
        Extract notes one by one using AppleScript (most reliable method)
        """
        notes = []
        
        # First, get the list of note IDs
        get_ids_script = '''
        tell application "Notes"
            set noteIds to {}
            repeat with eachNote in notes
                set end of noteIds to id of eachNote
            end repeat
            return noteIds
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', get_ids_script],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Error getting note IDs: {result.stderr}")
                return []
            
            # Parse IDs from output
            note_ids = result.stdout.strip().split(', ')
            
            # Extract each note individually
            for note_id in note_ids:
                note_data = self._extract_single_note(note_id.strip())
                if note_data:
                    notes.append(note_data)
                    print(f"Extracted note: {note_data['title']}")
            
        except Exception as e:
            print(f"Error extracting notes: {e}")
        
        return notes
    
    def _extract_single_note(self, note_id):
        """
        Extract a single note by ID using AppleScript
        """
        extract_script = f'''
        tell application "Notes"
            set targetNote to note id "{note_id}"
            set noteTitle to name of targetNote
            set noteBody to body of targetNote
            set noteCreated to creation date of targetNote
            set noteModified to modification date of targetNote
            set noteFolder to name of container of targetNote
            
            return noteTitle & "|||" & noteBody & "|||" & noteCreated & "|||" & noteModified & "|||" & noteFolder
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', extract_script],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return None
            
            # Parse the output
            parts = result.stdout.strip().split('|||')
            if len(parts) >= 5:
                # Clean HTML from body
                body_text = self._clean_html(parts[1])
                
                # Calculate word count
                word_count = len(body_text.split())
                
                # Parse dates
                created_date = self._parse_applescript_date(parts[2])
                modified_date = self._parse_applescript_date(parts[3])
                
                return {
                    'id': note_id,
                    'title': parts[0],
                    'content': body_text,
                    'created_at': created_date,
                    'updated_at': modified_date,
                    'folder': parts[4],
                    'word_count': word_count,
                    'tags': self._extract_tags_from_content(body_text)
                }
            
        except Exception as e:
            print(f"Error extracting note {note_id}: {e}")
        
        return None
    
    def _clean_html(self, html_content):
        """
        Remove HTML tags from note content
        """
        # Remove HTML tags
        clean_text = re.sub('<.*?>', '', html_content)
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        # Decode HTML entities
        clean_text = clean_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        return clean_text.strip()
    
    def _parse_applescript_date(self, date_str):
        """
        Parse AppleScript date format to ISO format
        """
        try:
            # AppleScript dates are in format like "Monday, November 25, 2024 at 2:30:45 PM"
            # This is a simplified parser - adjust as needed
            from dateutil import parser
            parsed_date = parser.parse(date_str)
            return parsed_date.isoformat()
        except:
            # Fallback to current date if parsing fails
            return datetime.now().isoformat()
    
    def _extract_tags_from_content(self, content):
        """
        Extract potential tags from content (hashtags or common patterns)
        """
        tags = []
        
        # Find hashtags
        hashtags = re.findall(r'#(\w+)', content)
        tags.extend(hashtags)
        
        # You can add more tag extraction logic here
        
        return list(set(tags))  # Remove duplicates
    
    def export_to_ghost_writer_format(self, notes, output_file='apple_notes_export.json'):
        """
        Export notes to Ghost Writer compatible JSON format
        """
        ghost_writer_data = {
            "exportDate": datetime.now().isoformat(),
            "type": "ghost_writer_import",
            "version": "1.0",
            "importType": "apple_notes_sync",
            "notes": []
        }
        
        for note in notes:
            ghost_note = {
                "id": note['id'],
                "title": note['title'],
                "content": note['content'],
                "tags": note['tags'],
                "createdAt": note['created_at'],
                "updatedAt": note['updated_at'],
                "wordCount": note['word_count'],
                "linkedBlogPosts": [],
                "metadata": {
                    "source": "Apple Notes",
                    "folder": note['folder'],
                    "originalId": note['id']
                }
            }
            ghost_writer_data['notes'].append(ghost_note)
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ghost_writer_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nExported {len(notes)} notes to {output_file}")
        return output_file
    
    def sync_with_existing(self, existing_file, notes):
        """
        Sync with existing Ghost Writer data to avoid duplicates
        """
        existing_data = None
        
        # Load existing data if file exists
        if os.path.exists(existing_file):
            with open(existing_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        if existing_data and 'notes' in existing_data:
            existing_ids = {note.get('metadata', {}).get('originalId') for note in existing_data['notes'] 
                          if note.get('metadata', {}).get('source') == 'Apple Notes'}
            
            # Filter out notes that already exist
            new_notes = [note for note in notes if note['id'] not in existing_ids]
            
            print(f"Found {len(new_notes)} new notes to sync")
            return new_notes
        
        return notes

def main():
    print("Apple Notes to Ghost Writer Sync Tool")
    print("=" * 50)
    
    extractor = AppleNotesExtractor()
    
    print("\nExtracting notes from Apple Notes...")
    notes = extractor.extract_notes_individually()
    
    if not notes:
        print("No notes found or error accessing Apple Notes")
        return
    
    print(f"\nSuccessfully extracted {len(notes)} notes")
    
    # Check for existing export to sync
    sync_file = "ghost_writer_sync.json"
    if os.path.exists(sync_file):
        print(f"\nFound existing sync file: {sync_file}")
        response = input("Do you want to sync with existing data? (y/n): ")
        if response.lower() == 'y':
            notes = extractor.sync_with_existing(sync_file, notes)
    
    # Export to Ghost Writer format
    output_file = extractor.export_to_ghost_writer_format(notes)
    
    print("\n✅ Export complete!")
    print(f"📄 File saved as: {output_file}")
    print("\nTo import into Ghost Writer:")
    print("1. Open Ghost Writer in your browser")
    print("2. Click the 'Import' button")
    print("3. Select 'Import Notes' as the import type")
    print("4. Choose the exported JSON file or paste its contents")
    print("5. Click 'Import Data'")
    
    # Optionally create a sync file for future runs
    if not os.path.exists(sync_file):
        response = input("\nCreate a sync file for future updates? (y/n): ")
        if response.lower() == 'y':
            import shutil
            shutil.copy(output_file, sync_file)
            print(f"Sync file created: {sync_file}")

if __name__ == "__main__":
    # Check if dateutil is installed
    try:
        import dateutil
    except ImportError:
        print("Please install python-dateutil first:")
        print("pip install python-dateutil")
        exit(1)
    
    main()
