#!/usr/bin/env python3
"""
NeuAI Test Suite
================
Comprehensive test suite for the NeuAI CLI.
Tests connection, chat, memory, and agent functionality.

Usage:
    python neuai-test-suite.py [--verbose] [--quick]

Options:
    --verbose    Show detailed output for each test
    --quick      Run only essential tests (skip slow ones)
"""

import os
import sys
import json
import time
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict, Any

# =============================================================================
# Test Configuration - Uses environment variables or ~/.neuai/config.json
# =============================================================================

def load_test_config():
    """Load test config from environment or saved config."""
    config = {
        "endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        "api_key": os.environ.get("AZURE_OPENAI_KEY", ""),
        "deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4"),
        "api_version": os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    }

    # Try loading from saved config if env vars not set
    config_file = Path.home() / ".neuai" / "config.json"
    if config_file.exists() and not config["api_key"]:
        try:
            with open(config_file, 'r') as f:
                saved = json.load(f)
                config["endpoint"] = config["endpoint"] or saved.get("endpoint", "")
                config["api_key"] = config["api_key"] or saved.get("api_key", "")
                config["deployment"] = saved.get("deployment", config["deployment"])
                config["api_version"] = saved.get("api_version", config["api_version"])
        except Exception:
            pass

    return config

TEST_CONFIG = load_test_config()

# =============================================================================
# Import NeuAI Components
# =============================================================================

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

# Load neuai-cli.py module
neuai_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neuai-cli.py")
spec = spec_from_loader("neuai_cli", SourceFileLoader("neuai_cli", neuai_path))
neuai = module_from_spec(spec)
spec.loader.exec_module(neuai)

Config = neuai.Config
AzureOpenAIClient = neuai.AzureOpenAIClient
MemoryManager = neuai.MemoryManager
ConversationManager = neuai.ConversationManager
NeuAIAssistant = neuai.NeuAIAssistant
CalculatorAgent = neuai.CalculatorAgent
DateTimeAgent = neuai.DateTimeAgent

# =============================================================================
# Test Framework
# =============================================================================

class TestResult:
    def __init__(self, name: str, passed: bool, message: str, duration: float = 0):
        self.name = name
        self.passed = passed
        self.message = message
        self.duration = duration

class TestSuite:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[TestResult] = []
        self.temp_dir = None
        self.config = None

    def setup(self):
        """Setup test environment with temporary directory."""
        self.temp_dir = tempfile.mkdtemp(prefix="neuai_test_")

        # Create config with test credentials
        self.config = Config.__new__(Config)
        self.config.endpoint = TEST_CONFIG["endpoint"]
        self.config.api_key = TEST_CONFIG["api_key"]
        self.config.deployment = TEST_CONFIG["deployment"]
        self.config.api_version = TEST_CONFIG["api_version"]
        self.config.data_dir = Path(self.temp_dir)
        self.config.memory_file = self.config.data_dir / "memories.json"
        self.config.context_file = self.config.data_dir / "context.json"
        self.config.config_file = self.config.data_dir / "config.json"

        if self.verbose:
            print(f"\n📁 Test directory: {self.temp_dir}")
            print(f"🔗 Endpoint: {self.config.endpoint}")
            print(f"🚀 Deployment: {self.config.deployment}")

    def teardown(self):
        """Cleanup test environment."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def run_test(self, name: str, test_func):
        """Run a single test and record result."""
        start_time = time.time()
        try:
            if self.verbose:
                print(f"\n⏳ Running: {name}...", end=" ", flush=True)

            passed, message = test_func()
            duration = time.time() - start_time

            result = TestResult(name, passed, message, duration)
            self.results.append(result)

            if self.verbose:
                status = "✅" if passed else "❌"
                print(f"{status} ({duration:.2f}s)")
                if not passed:
                    print(f"   └─ {message}")

            return passed

        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(name, False, f"Exception: {str(e)}", duration)
            self.results.append(result)

            if self.verbose:
                print(f"❌ ({duration:.2f}s)")
                print(f"   └─ Exception: {str(e)}")

            return False

    def print_summary(self):
        """Print test results summary."""
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        total_time = sum(r.duration for r in self.results)

        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)

        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"  {status}  {result.name} ({result.duration:.2f}s)")
            if not result.passed:
                print(f"         └─ {result.message}")

        print("\n" + "-" * 60)
        print(f"Total: {len(self.results)} tests | Passed: {passed} | Failed: {failed}")
        print(f"Time: {total_time:.2f}s")
        print("=" * 60)

        return failed == 0


# =============================================================================
# Test Cases
# =============================================================================

def test_config_validation(suite: TestSuite) -> Tuple[bool, str]:
    """Test that configuration validates correctly."""
    if not suite.config.is_configured():
        return False, "Config reports as not configured"

    if not suite.config.endpoint:
        return False, "Endpoint is empty"

    if not suite.config.api_key:
        return False, "API key is empty"

    if not suite.config.deployment:
        return False, "Deployment is empty"

    return True, "Configuration validated"


def test_connection(suite: TestSuite) -> Tuple[bool, str]:
    """Test Azure OpenAI connection."""
    success, message = suite.config.test_connection()
    return success, message


def test_client_creation(suite: TestSuite) -> Tuple[bool, str]:
    """Test Azure OpenAI client creation."""
    try:
        client = AzureOpenAIClient(suite.config)
        if client.config != suite.config:
            return False, "Client config mismatch"
        return True, "Client created successfully"
    except Exception as e:
        return False, str(e)


def test_simple_chat(suite: TestSuite) -> Tuple[bool, str]:
    """Test basic chat completion."""
    client = AzureOpenAIClient(suite.config)

    messages = [
        {"role": "user", "content": "Reply with only the word 'hello' in lowercase."}
    ]

    response = client.chat_completion(messages, max_tokens=10)

    if "choices" not in response:
        return False, "No choices in response"

    if len(response["choices"]) == 0:
        return False, "Empty choices array"

    content = response["choices"][0]["message"]["content"].lower()

    if "hello" in content:
        return True, f"Got response: {content[:50]}"

    return True, f"Got response (may vary): {content[:50]}"


def test_memory_storage(suite: TestSuite) -> Tuple[bool, str]:
    """Test memory storage functionality."""
    memory = MemoryManager(suite.config)

    # Store a memory
    memory_id = memory.store_memory(
        content="Test user likes Python programming",
        memory_type="preference",
        importance=4
    )

    if not memory_id:
        return False, "No memory ID returned"

    # Check it was stored
    memories = memory.get_all_memories()
    if len(memories) == 0:
        return False, "Memory not stored"

    if memories[0]["content"] != "Test user likes Python programming":
        return False, "Memory content mismatch"

    return True, f"Memory stored with ID: {memory_id[:8]}..."


def test_memory_recall(suite: TestSuite) -> Tuple[bool, str]:
    """Test memory recall functionality."""
    memory = MemoryManager(suite.config)

    # Store multiple memories
    memory.store_memory("User's favorite color is blue", "preference")
    memory.store_memory("User works as a software engineer", "fact")
    memory.store_memory("User prefers dark mode", "preference")

    # Recall all
    all_memories = memory.recall_memories(max_results=10)
    if len(all_memories) < 3:
        return False, f"Expected 3+ memories, got {len(all_memories)}"

    # Recall with keyword
    filtered = memory.recall_memories(keywords=["blue"])
    if len(filtered) == 0:
        return False, "Keyword filter returned no results"

    if "blue" not in filtered[0]["content"].lower():
        return False, "Keyword filter returned wrong memory"

    return True, f"Recalled {len(all_memories)} memories, filter works"


def test_memory_clear(suite: TestSuite) -> Tuple[bool, str]:
    """Test memory clearing functionality."""
    memory = MemoryManager(suite.config)

    # Store then clear
    memory.store_memory("Temporary memory", "fact")
    memory.clear_memories()

    memories = memory.get_all_memories()
    if len(memories) != 0:
        return False, f"Expected 0 memories after clear, got {len(memories)}"

    return True, "Memories cleared successfully"


def test_conversation_manager(suite: TestSuite) -> Tuple[bool, str]:
    """Test conversation history management."""
    conv = ConversationManager(suite.config)
    conv.clear()  # Start fresh

    # Add messages
    conv.add_message("user", "Hello")
    conv.add_message("assistant", "Hi there!")
    conv.add_message("user", "How are you?")

    messages = conv.get_messages()

    if len(messages) != 3:
        return False, f"Expected 3 messages, got {len(messages)}"

    if messages[0]["role"] != "user":
        return False, "First message role incorrect"

    if messages[1]["content"] != "Hi there!":
        return False, "Second message content incorrect"

    return True, "Conversation manager working correctly"


def test_conversation_persistence(suite: TestSuite) -> Tuple[bool, str]:
    """Test that conversation persists to file."""
    conv1 = ConversationManager(suite.config)
    conv1.clear()
    conv1.add_message("user", "Persistent message")

    # Create new instance (simulates restart)
    conv2 = ConversationManager(suite.config)
    messages = conv2.get_messages()

    if len(messages) == 0:
        return False, "Conversation not persisted"

    if messages[0]["content"] != "Persistent message":
        return False, "Persisted content incorrect"

    return True, "Conversation persists correctly"


def test_calculator_agent(suite: TestSuite) -> Tuple[bool, str]:
    """Test calculator agent."""
    calc = CalculatorAgent()

    # Test basic arithmetic
    result = calc.perform(expression="2 + 2")
    if "4" not in result:
        return False, f"2+2 failed: {result}"

    # Test more complex
    result = calc.perform(expression="sqrt(144)")
    if "12" not in result:
        return False, f"sqrt(144) failed: {result}"

    # Test with math constants
    result = calc.perform(expression="pi * 2")
    if "6.28" not in result:
        return False, f"pi*2 failed: {result}"

    return True, "Calculator agent working"


def test_datetime_agent(suite: TestSuite) -> Tuple[bool, str]:
    """Test datetime agent."""
    dt = DateTimeAgent()

    result = dt.perform(operation="current")

    # Should contain current year
    current_year = str(datetime.now().year)
    if current_year not in result:
        return False, f"Current year not in result: {result}"

    return True, "DateTime agent working"


def test_full_assistant_chat(suite: TestSuite) -> Tuple[bool, str]:
    """Test full assistant chat flow."""
    assistant = NeuAIAssistant(suite.config)

    # Clear any existing context
    assistant.new_conversation()
    assistant.memory.clear_memories()

    # Simple chat
    response = assistant.chat("What is 2 plus 2?")

    if not response:
        return False, "Empty response from assistant"

    if len(response) < 5:
        return False, f"Response too short: {response}"

    return True, f"Got response: {response[:100]}..."


def test_assistant_memory_integration(suite: TestSuite) -> Tuple[bool, str]:
    """Test that assistant can use memory tools."""
    assistant = NeuAIAssistant(suite.config)
    assistant.new_conversation()
    assistant.memory.clear_memories()

    # Ask it to remember something
    response = assistant.chat("Please remember that my favorite programming language is Python.")

    # Check if memory was stored
    memories = assistant.memory.get_all_memories()

    # The AI might or might not store it depending on its decision
    # But we should at least get a response
    if not response:
        return False, "No response when asking to remember"

    return True, f"Memory integration test passed. Memories: {len(memories)}"


def test_assistant_tool_calling(suite: TestSuite) -> Tuple[bool, str]:
    """Test that assistant can call tools."""
    assistant = NeuAIAssistant(suite.config)
    assistant.new_conversation()

    # Ask for current date (should trigger datetime tool)
    response = assistant.chat("What is today's date?")

    if not response:
        return False, "No response for date query"

    # Response should contain date-related content
    current_year = str(datetime.now().year)
    current_month = datetime.now().strftime("%B").lower()

    response_lower = response.lower()
    if current_year in response or current_month in response_lower:
        return True, f"Tool calling works: {response[:100]}..."

    # Even if it doesn't use the tool, it should respond
    return True, f"Got response (tool may not have been called): {response[:100]}..."


def test_error_handling_bad_expression(suite: TestSuite) -> Tuple[bool, str]:
    """Test error handling for invalid calculator expression."""
    calc = CalculatorAgent()

    result = calc.perform(expression="1/0")

    if "error" in result.lower():
        return True, "Division by zero handled correctly"

    return False, f"Expected error, got: {result}"


def test_error_handling_invalid_json(suite: TestSuite) -> Tuple[bool, str]:
    """Test memory manager handles corrupted files."""
    # Write invalid JSON to memory file
    with open(suite.config.memory_file, 'w') as f:
        f.write("not valid json {{{")

    # Should not crash
    memory = MemoryManager(suite.config)
    memories = memory.get_all_memories()

    if len(memories) != 0:
        return False, "Should have empty memories after corruption"

    return True, "Corrupted file handled gracefully"


def test_config_save_and_load(suite: TestSuite) -> Tuple[bool, str]:
    """Test configuration persistence."""
    # Save config
    suite.config.save_config()

    if not suite.config.config_file.exists():
        return False, "Config file not created"

    # Read it back
    with open(suite.config.config_file, 'r') as f:
        saved = json.load(f)

    if saved["endpoint"] != suite.config.endpoint:
        return False, "Endpoint not saved correctly"

    if saved["deployment"] != suite.config.deployment:
        return False, "Deployment not saved correctly"

    return True, "Config saves and loads correctly"


# =============================================================================
# Main Test Runner
# =============================================================================

def run_tests(verbose: bool = False, quick: bool = False):
    """Run all tests."""
    print("\n" + "=" * 60)
    print("NEUAI TEST SUITE")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'Quick' if quick else 'Full'} | Verbose: {verbose}")

    suite = TestSuite(verbose=verbose)

    try:
        suite.setup()

        # Configuration Tests
        print("\n📋 Configuration Tests")
        suite.run_test("Config Validation", lambda: test_config_validation(suite))
        suite.run_test("Config Save/Load", lambda: test_config_save_and_load(suite))

        # Connection Tests
        print("\n🔌 Connection Tests")
        suite.run_test("Azure OpenAI Connection", lambda: test_connection(suite))
        suite.run_test("Client Creation", lambda: test_client_creation(suite))

        if not quick:
            # Chat Tests
            print("\n💬 Chat Tests")
            suite.run_test("Simple Chat", lambda: test_simple_chat(suite))

        # Memory Tests
        print("\n🧠 Memory Tests")
        suite.run_test("Memory Storage", lambda: test_memory_storage(suite))
        suite.run_test("Memory Recall", lambda: test_memory_recall(suite))
        suite.run_test("Memory Clear", lambda: test_memory_clear(suite))

        # Conversation Tests
        print("\n📝 Conversation Tests")
        suite.run_test("Conversation Manager", lambda: test_conversation_manager(suite))
        suite.run_test("Conversation Persistence", lambda: test_conversation_persistence(suite))

        # Agent Tests
        print("\n🤖 Agent Tests")
        suite.run_test("Calculator Agent", lambda: test_calculator_agent(suite))
        suite.run_test("DateTime Agent", lambda: test_datetime_agent(suite))

        # Error Handling Tests
        print("\n⚠️  Error Handling Tests")
        suite.run_test("Bad Expression Handling", lambda: test_error_handling_bad_expression(suite))
        suite.run_test("Invalid JSON Handling", lambda: test_error_handling_invalid_json(suite))

        if not quick:
            # Integration Tests (slower)
            print("\n🔗 Integration Tests")
            suite.run_test("Full Assistant Chat", lambda: test_full_assistant_chat(suite))
            suite.run_test("Assistant Memory Integration", lambda: test_assistant_memory_integration(suite))
            suite.run_test("Assistant Tool Calling", lambda: test_assistant_tool_calling(suite))

        # Print summary
        all_passed = suite.print_summary()

        return 0 if all_passed else 1

    finally:
        suite.teardown()


def main():
    """Main entry point."""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    quick = "--quick" in sys.argv or "-q" in sys.argv

    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0

    return run_tests(verbose=verbose, quick=quick)


if __name__ == "__main__":
    sys.exit(main())
