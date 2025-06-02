# Figma Design Specifications

## Typography System

### Fonts
```css
Font Family: Inter
Weights: 400 (Regular), 500 (Medium), 600 (SemiBold)

Title Text:
- Size: 24px
- Weight: 600
- Line Height: 32px

Subtitle Text:
- Size: 16px
- Weight: 500
- Line Height: 24px

Body Text:
- Size: 14px
- Weight: 400
- Line Height: 20px

Metric Text:
- Size: 12px
- Weight: 500
- Line Height: 16px
```

## Color System

### Primary Colors
```css
Blue:
- Primary: #228BE6
- Light: #E7F5FF
- Dark: #1971C2

Background:
- Page: #F8F9FA
- Card: #FFFFFF
```

### Gray Scale
```css
Gray:
- 900: #212529 (Text Primary)
- 700: #495057 (Text Secondary)
- 600: #868E96 (Text Tertiary)
- 200: #E9ECEF (Borders)
- 100: #F1F3F5 (Selected State)
```

## Layout Specifications

### Grid System
```css
Container:
- Max Width: 1440px
- Padding: 24px

Sidebar:
- Width: 240px
- Fixed Position

Main Content:
- Margin Left: 264px
- Padding: 24px
```

### Component Spacing
```css
Vertical Spacing:
- Between Sections: 24px
- Between Items: 16px
- Inside Components: 8px

Horizontal Spacing:
- Between Components: 24px
- Component Padding: 24px
```

## Interactive Elements

### States
```css
Buttons:
- Default: #FFFFFF
- Hover: #F1F3F5
- Active: #E7F5FF
- Disabled: #F8F9FA

Cards:
- Default: #FFFFFF
- Hover: Box-shadow: 0 2px 8px rgba(0,0,0,0.1)
```

## Component Specifications

### Navigation Item
```css
Height: 40px
Border Radius: 8px
Padding: 0 24px
Font: Inter 16px Medium
```

### Metric Card
```css
Width: 240px
Height: 100px
Border Radius: 8px
Background: #FFFFFF
Border: 1px solid #E9ECEF
Padding: 24px
```

### Flow Component
```css
Width: 200px
Height: 120px
Border Radius: 8px
Background: #E7F5FF
Border: 1px solid #228BE6
Padding: 24px
```

## Animation Specifications

### Transitions
```css
Default Transition:
- Duration: 200ms
- Timing: ease-in-out

Hover States:
- Scale: 1.02
- Duration: 150ms
```

## Responsive Breakpoints
```css
Desktop: 1440px
Laptop: 1024px
Tablet: 768px
Mobile: 375px
```