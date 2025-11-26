# Dynamic Living Strategic Document System

## 🎯 Overview

This is a **fully dynamic, schema-driven document system** where EVERY aspect of the document - structure, styling, components, data, and behavior - is defined through JSON configuration. Think of it as "documents as code" where you can completely transform the entire application just by loading a different JSON schema.

## 🚀 Key Features

### Complete Dynamic Control
- **Structure**: Define sections, components, and layout through JSON
- **Styling**: Customize colors, gradients, and theming
- **Components**: Choose from 15+ dynamic component types
- **Data**: All form inputs, calculations, and metrics
- **Behavior**: Interactive elements, calculations, and workflows

### Powerful Components
1. **Metrics Dashboard** - Real-time KPI displays with color coding
2. **Interactive Charts** - Bar charts, line charts, growth projections
3. **Progress Trackers** - Multi-step progress visualization
4. **Scenario Modeling** - Multi-scenario comparison with sliders
5. **Timelines** - Milestone and roadmap visualization
6. **Financial Calculators** - Runway, growth, ROI, break-even
7. **Decision Trees** - Interactive decision-making frameworks
8. **Risk Analysis** - Risk matrices and mitigation planning
9. **Form Inputs** - Text, numbers, textareas with auto-save
10. **Custom HTML** - Inject any custom content

## 📋 How It Works

### Architecture

```
JSON Schema Definition
    ↓
DynamicDocument Engine
    ↓
Component Renderer
    ↓
Live HTML/CSS/JS
    ↓
Auto-save to localStorage
```

The `DynamicDocument` class:
1. Loads schema and data from localStorage or default
2. Applies theme colors to CSS variables
3. Renders all components dynamically
4. Binds event listeners and auto-save
5. Handles real-time calculations
6. Manages import/export

### Schema Structure

```json
{
  "meta": {
    "title": "Document Title",
    "subtitle": "Document description",
    "version": "1.0.0"
  },
  "theme": {
    "primary": "#color",
    "headerGradient": "linear-gradient(...)",
    "headerTextColor": "#color"
  },
  "header": {
    "enabled": true,
    "showInput": true,
    "showStatus": true
  },
  "sections": [
    {
      "id": "section-id",
      "title": "Section Title",
      "icon": "📊",
      "active": true,
      "components": [...]
    }
  ],
  "actions": [...]
}
```

## 🎨 Available Component Types

### 1. Card Container
```json
{
  "type": "card",
  "icon": "🎯",
  "title": "Card Title",
  "content": [...]
}
```

### 2. Metrics Display
```json
{
  "type": "metrics",
  "metrics": [
    {
      "id": "revenue",
      "label": "Monthly Revenue",
      "value": "$50,000",
      "color": "success",
      "change": "+15% MoM"
    }
  ]
}
```

### 3. Form Inputs

**Text Input:**
```json
{
  "type": "input",
  "id": "companyName",
  "label": "Company Name",
  "placeholder": "Enter name..."
}
```

**Number Input:**
```json
{
  "type": "number",
  "id": "currentCash",
  "label": "Cash ($)",
  "value": 100000
}
```

**Textarea:**
```json
{
  "type": "textarea",
  "id": "mission",
  "label": "Mission Statement",
  "rows": 3
}
```

### 4. Slider
```json
{
  "type": "slider",
  "id": "growthRate",
  "label": "Growth Rate",
  "min": 0,
  "max": 100,
  "value": 15,
  "unit": "%"
}
```

### 5. Progress Tracker
```json
{
  "type": "progress",
  "steps": [
    { "id": 1, "label": "Define", "status": "completed" },
    { "id": 2, "label": "Plan", "status": "current" },
    { "id": 3, "label": "Execute", "status": "pending" }
  ]
}
```

### 6. Timeline
```json
{
  "type": "timeline",
  "items": [
    {
      "date": "Q1 2024",
      "title": "Launch",
      "description": "Product launch",
      "status": "completed"
    }
  ]
}
```

### 7. Chart
```json
{
  "type": "chart",
  "chartType": "bar",
  "id": "growthChart",
  "computed": true
}
```

### 8. Grid Layout
```json
{
  "type": "grid",
  "columns": 3,
  "items": [...]
}
```

### 9. Scenario Comparison
```json
{
  "type": "scenarios",
  "scenarios": [
    {
      "id": "pessimistic",
      "label": "😰 Pessimistic",
      "color": "#ef4444",
      "factor": 0.7
    }
  ]
}
```

### 10. Custom HTML
```json
{
  "type": "html",
  "html": "<div>Custom HTML content</div>"
}
```

## 💡 Usage Examples

### Example 1: Simple Financial Dashboard

```json
{
  "meta": {
    "title": "My Startup Finances"
  },
  "theme": {
    "primary": "#3b82f6"
  },
  "sections": [
    {
      "id": "dashboard",
      "title": "Dashboard",
      "icon": "📊",
      "active": true,
      "components": [
        {
          "type": "card",
          "title": "Key Metrics",
          "content": [
            {
              "type": "metrics",
              "metrics": [
                {
                  "id": "mrr",
                  "label": "MRR",
                  "value": "$10k",
                  "color": "success"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Example 2: Complete Strategic Plan

See `advanced-schema-example.json` for a full-featured example with:
- Executive summary with vision/mission
- Financial analytics with multiple calculators
- Scenario modeling with 5 scenarios
- Product roadmap with timeline
- Team structure and hiring plan
- Comprehensive risk register

## 🔧 How to Use

### 1. Basic Setup
```html
<!-- Open dynamic-living-document.html in browser -->
<!-- Document loads with default schema -->
```

### 2. Import Custom Schema
1. Click "📥 Import" button
2. Select a JSON file (schema + data)
3. Document completely transforms to new structure
4. All data auto-saves to localStorage

### 3. Customize Theme
Modify the `theme` object in your JSON:
```json
{
  "theme": {
    "primary": "#6366f1",
    "secondary": "#ec4899",
    "success": "#10b981",
    "headerGradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
  }
}
```

### 4. Add New Section
```json
{
  "sections": [
    {
      "id": "custom",
      "title": "My Section",
      "icon": "⭐",
      "active": false,
      "components": [
        {
          "type": "card",
          "title": "Custom Card",
          "content": [...]
        }
      ]
    }
  ]
}
```

### 5. Export Everything
- **Export JSON**: Complete schema + data for backup/sharing
- **Export HTML**: Self-contained HTML file
- **Print**: Generate PDF via print dialog

## 🎯 Real-World Use Cases

### 1. Startup Strategic Planning
- Financial modeling and projections
- Fundraising calculator
- Scenario planning
- Risk assessment
- Roadmap tracking

### 2. Product Launch Planning
- Go-to-market strategy
- Timeline and milestones
- Resource allocation
- Success metrics

### 3. Investment Analysis
- ROI calculations
- Break-even analysis
- Scenario modeling
- Risk matrices

### 4. Personal Finance
- Budget tracking
- Investment portfolio
- Goal planning
- Net worth tracking

### 5. Project Planning
- Task timelines
- Resource allocation
- Budget tracking
- Risk management

## 🔄 Data Flow

```
User Input
    ↓
Event Listener
    ↓
Update this.data
    ↓
Save to localStorage
    ↓
Recalculate computed values
    ↓
Update UI metrics/charts
    ↓
Show "Saved" status
```

## 📊 Computed Metrics

The system automatically calculates:

1. **Runway**: `cash / (burn - revenue)`
2. **Growth Projections**: MRR × (1 + growth%)^months
3. **LTV**: ARPU × (1 / churn_rate)
4. **LTV:CAC Ratio**: LTV / CAC
5. **Scenario Variations**: Base × scenario_factor

Add custom calculations by extending the `recalculate()` method.

## 🎨 Theming System

Colors are applied via CSS variables:
```css
:root {
  --primary: #2563eb;
  --success: #10b981;
  --warning: #f59e0b;
  /* ... */
}
```

Change theme in JSON, system updates all CSS variables automatically.

## 💾 Data Persistence

**Auto-save:** Every input change saves to localStorage
- Schema: `localStorage.livingDocumentSchema`
- Data: `localStorage.livingDocumentData`

**Import/Export:**
- Export includes both schema AND data
- Import restores complete state
- Page reload preserves everything

## 🚀 Advanced Customization

### Add New Component Type

1. Add to schema:
```json
{
  "type": "myCustomComponent",
  "config": {...}
}
```

2. Add renderer in `DynamicDocument`:
```javascript
renderContent(item) {
  switch (item.type) {
    case 'myCustomComponent':
      return this.renderMyCustom(item);
    // ...
  }
}

renderMyCustom(item) {
  const el = document.createElement('div');
  // Build your component
  return el;
}
```

### Add Custom Calculations

Extend `recalculate()`:
```javascript
recalculate() {
  // Existing calculations...

  // Add yours:
  const customMetric = this.data.x * this.data.y;
  this.updateMetric('customId', customMetric);
}
```

### Add Custom Actions

1. Define in schema:
```json
{
  "actions": [
    {
      "id": "custom-action",
      "label": "My Action",
      "action": "myCustomAction"
    }
  ]
}
```

2. Handle in code:
```javascript
handleAction(action) {
  switch (action) {
    case 'myCustomAction':
      // Your logic
      break;
  }
}
```

## 📱 Responsive Design

All components are mobile-responsive:
- Metrics stack vertically on small screens
- Grids collapse to single column
- Charts scale proportionally
- Navigation becomes horizontal scroll

## 🖨️ Print Support

Print styles automatically:
- Hide navigation and action buttons
- Show all sections
- Adjust for page breaks
- Optimize for black & white

## 🎯 Best Practices

1. **Start Simple**: Use default schema, customize gradually
2. **Name IDs Clearly**: Use descriptive IDs for metrics/inputs
3. **Group Related Items**: Use cards to organize content
4. **Test Scenarios**: Verify calculations with sample data
5. **Export Often**: Backup your schema+data regularly
6. **Mobile First**: Test on small screens
7. **Color Accessibility**: Ensure sufficient contrast
8. **Document Assumptions**: Add notes to complex calculations

## 🔍 Troubleshooting

**Document doesn't load:**
- Check browser console for errors
- Verify JSON syntax (use JSONLint)
- Clear localStorage and refresh

**Metrics not updating:**
- Check `recalculate()` is called on input
- Verify ID matches between input and metric
- Check for JavaScript errors

**Import fails:**
- Ensure JSON includes `schema` and `data` keys
- Validate JSON structure
- Check file encoding (UTF-8)

**Styling issues:**
- Verify theme colors are valid hex codes
- Check CSS variable names
- Clear browser cache

## 🎓 Learning Path

1. **Beginner**: Open default, edit company name, add metrics
2. **Intermediate**: Customize theme, add sections, create cards
3. **Advanced**: Build custom schema, add component types
4. **Expert**: Extend calculations, create specialized templates

## 🌟 Examples Included

1. **default schema** (in code): Basic strategic planning template
2. **advanced-schema-example.json**: TaskFlow AI complete strategic plan
3. **example-strategic-plan.json**: Full data export with all fields

## 📚 Resources

- **JSON Schema**: Define document structure
- **CSS Variables**: Theme customization
- **LocalStorage API**: Data persistence
- **ES6 Classes**: Modular architecture

## 🔮 Future Enhancements

Potential additions:
- Real-time collaboration
- Version history
- Template marketplace
- AI-powered insights
- Database integration
- API endpoints
- Chart library integration
- Conditional logic
- Formula support

## 🤝 Contributing

To extend this system:
1. Fork the HTML file
2. Add new component types
3. Extend calculation engine
4. Share schemas with community

## 📄 License

Open source - use freely for any purpose.

---

## Quick Start Checklist

- [ ] Open `dynamic-living-document.html` in browser
- [ ] Enter company name in header
- [ ] Fill out financial inputs
- [ ] Adjust scenario sliders
- [ ] Review calculated metrics
- [ ] Add timeline milestones
- [ ] Document risks
- [ ] Export JSON for backup
- [ ] Customize theme colors
- [ ] Import advanced example
- [ ] Create custom schema
- [ ] Share with team

**Ready to build your living strategic document!** 🚀
