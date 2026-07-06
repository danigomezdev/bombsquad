# Polish UI Builder for BombSquad

A powerful visual interface builder that allows you to create and customize BombSquad user interfaces with ease through an intuitive graphical editor.

## Description

Polish is a comprehensive UI development tool that revolutionizes how you create interfaces for BombSquad mods. It provides a real-time visual editor where you can drag, drop, and customize widgets without writing code, then export fully functional Python code for your mods.

## Features

- **Visual UI Builder**: Create interfaces by visually placing and arranging widgets
- **Real-time Editing**: See changes instantly as you modify widget properties
- **Widget Library**: Access all BombSquad widget types (buttons, text, images, scroll areas, etc.)
- **Property Inspector**: Modify position, size, colors, textures, and other properties visually
- **Grid System**: Enable grid snapping for precise alignment
- **Animation Support**: Configure entrance and exit animations for your interfaces
- **Code Export**: Generate clean, ready-to-use Python code from your designs
- **Copy to Clipboard**: Copy generated code directly to clipboard
- **Widget Presets**: Pre-built templates for common UI elements
- **Widget Management**: Copy, delete, and manage individual widgets
- **Parent-Child Relationships**: Easily set up widget hierarchies

## Installation

1. Download the `polish.py` file
2. Place it in your BombSquad mods folder (`ba_data/python`)
3. Ensure you have API version 9 or compatible version of BombSquad
4. Restart BombSquad

## Usage

### Starting the Editor

1. Launch BombSquad with the mod installed
2. Open the developer console (usually F2 or ~ key)
3. Type `Polish()` and press Enter
4. The Polish UI Builder interface will appear

### Main Interface Sections

#### File Menu
- **Export Code**: Generate and save Python code to a file
- **Copy Code**: Copy generated Python code to clipboard
- **Exit**: Close the Polish editor

#### Root Configuration
- Set the main container size and position
- Configure stack offset for proper positioning
- Modify root widget properties

#### Animation Settings
- Set entrance transitions (`in_scale`, `in_left`, `in_right`)
- Set exit animations (`out_scale`, `out_left`, `out_right`)
- Preview animations in real-time

#### Widget Management
- **Add Widget**: Choose from all available widget types
- **Presets**: Use pre-built widget templates
- **Grid**: Enable/disable grid snapping and configure grid size

### Creating Your First Interface

1. **Start with Root**: Configure your main container size and position
2. **Add Widgets**: Click "Widget" to add buttons, text, images, etc.
3. **Position Elements**: Use arrow keys or direct input to position widgets
4. **Customize Properties**: Select any widget to modify its properties
5. **Set Animations**: Configure how your interface enters and exits
6. **Export Code**: Generate Python code for your creation

### Widget Types Available

- **ButtonWidget**: Interactive buttons with various styles
- **TextWidget**: Labels, titles, and editable text fields
- **ImageWidget**: Display textures and images
- **ContainerWidget**: Group and organize other widgets
- **ScrollWidget**: Create scrollable areas
- **CheckboxWidget**: Toggle switches
- **And more**: All BombSquad widget types are supported

### Property Editing

When you select any widget, you can modify:

- **Position**: X and Y coordinates with precision controls
- **Size**: Width and height (or single value for square widgets)
- **Colors**: Background and text colors
- **Textures**: Apply any available texture
- **Text Content**: Labels and text values
- **Parent Relationships**: Set widget hierarchies
- **And dozens more properties**

### Using Presets

The preset system includes ready-to-use templates:

- **Back Buttons**: Small and large back buttons
- **Slim Buttons**: Modern square-styled buttons
- **Agent Icons**: Character icons with masking
- **Text Boxes**: Editable text fields
- **Titles**: Large formatted text
- **Separators**: Horizontal and vertical dividers

### Grid System

- Enable grid overlay for precise alignment
- Customizable grid density (5x5 default)
- Visual alignment guides
- Snap-to-grid functionality

### Code Generation

The generated code includes:

- Proper import statements for all used widgets
- Widget hierarchy preservation
- All configured properties and values
- Animation transitions
- Clean, readable Python code
- Ready-to-use `make()` function

## Technical Details

### Architecture

Polish implements a sophisticated object-oriented system:

- **Visual Editor**: Real-time WYSIWYG interface builder
- **Widget Registry**: Tracks all created widgets and their properties
- **Property System**: Dynamic property inspection and modification
- **Code Generator**: Converts visual designs to executable Python code
- **Animation Engine**: Preview and configure UI transitions

### Key Components

- **Polish Class**: Main editor controller and interface
- **File Manager**: Code export and clipboard operations
- **Widget Manager**: Individual widget property editing
- **Preset System**: Template-based widget creation
- **Grid Manager**: Visual alignment tools
- **Animation Controller**: Transition configuration
- **Root Configurator**: Main container settings

### Data Persistence

- Editor state maintained during session
- Configuration auto-saves in BombSquad config
- Export generates permanent Python files

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup
- Basic understanding of BombSquad UI system (helpful but not required)

## Compatibility

- Works with all BombSquad versions supporting API 9
- Compatible with most other UI mods
- Generated code works in any BombSquad mod environment
- Supports all standard BombSquad widgets and textures

## Performance Considerations

- **Editor Performance**: Optimized for smooth real-time editing
- **Memory Usage**: Efficient widget management and cleanup
- **Export Quality**: Generates optimized, clean code
- **Runtime**: No performance impact on generated interfaces

## Use Cases

### For Mod Developers
- Rapid UI prototyping and development
- Learning BombSquad UI system through visual examples
- Creating complex interfaces without memorizing widget APIs
- Maintaining consistent UI patterns across mods

### For Beginners
- Introduction to BombSquad UI programming
- Visual feedback while learning widget properties
- Template-based starting points for common elements
- Error-free code generation

### For Advanced Users
- Complex layout planning and testing
- Animation timing and transition preview
- Widget hierarchy visualization
- Rapid iteration and experimentation

## Important Notes

- Generated code requires the same textures to be available in your mod
- Some advanced widget properties may require manual code tweaking
- Parent-child relationships are automatically handled in code generation
- Animation names must match BombSquad's supported transition types
- The editor itself is a BombSquad UI, demonstrating its own capabilities

## Troubleshooting

### Common Issues:

- **Editor won't start**: Ensure correct API version and proper file placement
- **Widgets not appearing**: Check that you've added widgets to your root container
- **Code errors**: Verify all required textures exist in your mod
- **Performance issues**: Reduce grid density or number of visible widgets

### Export Problems:

- **Missing imports**: All required imports are automatically included
- **Parent errors**: Widget hierarchies are automatically resolved
- **Animation issues**: Ensure transition names match BombSquad's animation system

## Example Workflow

1. **Plan**: Sketch your interface layout
2. **Setup**: Configure root container size and position
3. **Build**: Add and arrange widgets using the visual editor
4. **Test**: Preview animations and interactions
5. **Refine**: Adjust properties and positioning
6. **Export**: Generate Python code for your mod
7. **Integrate**: Add the generated `make()` function to your mod

## Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/e5a0b385-0672-451a-8414-413b3dff86f0" width="49%" />
  <img src="https://github.com/user-attachments/assets/70aed00c-d71a-42fc-8f0e-307eea39a5cd" width="49%" />
  <br>
  <img src="https://github.com/user-attachments/assets/993e4012-3cdf-4e37-8b76-d90f20a58cd2" width="49%" />
  <img src="https://github.com/user-attachments/assets/e937fd20-01ac-4529-8e6c-31848551e131" width="49%" />
  <br>
  <img src="https://github.com/user-attachments/assets/86dc8fc7-c151-434f-b9ab-c2f5675483be" width="49%" />
  <img src="https://github.com/user-attachments/assets/9e4e48a5-e843-4b0a-9ffd-83d0ab5fa6a5" width="49%" />
</p>

## Video

https://github.com/user-attachments/assets/69d13dfe-98bf-4b65-8c59-58c433534b90

## Credits

Created by the [BrotherBoard](https://github.com/BrotherBoard)  
Forked by [Less](https://github.com/danigomezdev)
