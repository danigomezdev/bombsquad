# Auto Respond for BombSquad

An intelligent automated response system that automatically replies to specific chat messages with customizable responses, perfect for handling common questions, greetings, and interactions.

## Description

Auto Respond is a sophisticated chat automation mod that monitors game chat for specific trigger phrases and automatically sends pre-configured responses. This is ideal for server hosts, community managers, or any player who wants to streamline common interactions without manual typing.

## Features

- **Smart Trigger System**: Respond to exact matches or partial text in messages
- **Customizable Responses**: Create personalized replies with dynamic placeholders
- **Adjustable Timing**: Set precise delay times for responses
- **Case Sensitivity Options**: Choose between case-sensitive or case-insensitive matching
- **Multiple Response Types**: Support for exact matches and wildcard/partial matches
- **Placeholder Support**: Dynamic text replacement with:
  - `%m`: Your V2 account name
  - `%s`: Sender's name
  - `%t`: Current time (HH:MM:SS)
- **Visual Feedback**: Notifications when responses are triggered
- **Audio Alerts**: Optional sound notifications
- **Self-Response Control**: Choose whether to respond to your own messages
- **Easy Management**: Simple interface for adding, removing, and managing responses

## Installation

1. Download the `AutoRespond.py` file
2. Place it in your BombSquad mods folder
3. Ensure you have API version 9 or compatible version of BombSquad
4. Restart BombSquad

## Usage

### Accessing the Auto Respond Interface
1. Launch BombSquad with the mod installed
2. Open the party window (default Tab key)
3. Click the new "Auto" button in the interface
4. The Auto Respond control panel will open

### Main Interface Sections

#### Add Responses
- **If found**: The trigger phrase that will activate the response
- **Respond with**: The message to send when triggered
- **After seconds**: Delay before sending the response
- **Search in message**: Enable wildcard matching (respond if trigger appears anywhere in message)

#### Manage Responses
- **Nuke**: Remove existing triggers and responses
- **List**: View all configured triggers and responses
- **Tune**: Adjust settings and preferences

#### Settings (Tune)
- **Notify upon responding**: Show notification when response is sent
- **Ding upon responding**: Play sound when response is triggered
- **Respond to [your name]**: Allow responses to your own messages
- **Case sensitive**: Make trigger matching case-sensitive

## Configuration Examples

### Basic Greeting Response
- Trigger: "hello"
- Response: "Hello %s! Welcome to the game!"
- Delay: 0.5 seconds
- Wildcard: No

### Information Response
- Trigger: "how to play"
- Response: "Check controls in settings! Use WASD to move, space to jump."
- Delay: 1.0 seconds
- Wildcard: Yes

### Time-based Response
- Trigger: "what time"
- Response: "It's currently %t. Enjoy your game!"
- Delay: 0.3 seconds
- Wildcard: Yes

### Server Information
- Trigger: "server info"
- Response: "This server is hosted by %m. Have fun!"
- Delay: 0.5 seconds
- Wildcard: No

## Advanced Features

### Placeholder System
The mod supports dynamic text replacement:
- `%m` - Your V2 account name (automatically detects if signed in)
- `%s` - The name of the person who sent the triggering message
- `%t` - Current time in 24-hour format (HH:MM:SS)

### Response Timing
- Set delays from 0.1 to any number of seconds
- Prevents spam by staggering responses
- Allows natural conversation flow

### Matching Modes
- **Exact Match**: Only responds to exact trigger phrases
- **Wildcard Match**: Responds if trigger appears anywhere in message
- **Case Sensitivity**: Optional case-sensitive matching

## Requirements

- BombSquad version with API 9 support
- Python modding environment setup
- Active chat session for response monitoring

## Technical Details

This mod implements a sophisticated chat monitoring system:

- **Real-time Chat Analysis**: Monitors all incoming chat messages
- **Pattern Matching**: Efficient trigger detection with multiple matching modes
- **Dynamic Text Processing**: Real-time placeholder replacement
- **Thread-safe Operations**: Safe message handling across game sessions
- **Persistent Configuration**: Saves triggers and settings between sessions
- **UI Integration**: Seamless integration with BombSquad's party interface

## Use Cases

### For Server Hosts:
- Automated welcome messages for new players
- Frequently asked questions responses
- Server rule reminders
- Event announcements

### For Community Managers:
- Standardized responses to common questions
- Community guideline reminders
- Welcome messages for regular members
- Tournament information

### For Regular Players:
- Quick responses to friends' greetings
- Automated answers to common game questions
- Fun interactive responses
- Time-saving for repetitive conversations

### For Content Creators:
- Consistent responses during streams
- Automated engagement with viewers
- Brand messaging consistency
- Time management during busy sessions

## Configuration Management

### Adding Responses:
1. Click "Add" in the Auto Respond interface
2. Enter trigger phrase in "If found"
3. Enter response in "Respond with"
4. Set delay time
5. Choose wildcard option if needed
6. Click "Add" to save

### Managing Responses:
- **List**: View all triggers and their responses
- **Nuke**: Remove specific triggers
- **Tune**: Adjust global behavior settings

### Settings Options:
- **Notifications**: Control when you're notified about responses
- **Sounds**: Enable/disable audio feedback
- **Self-Response**: Control whether you respond to your own messages
- **Case Sensitivity**: Adjust matching strictness

## Performance Considerations

- **Minimal Impact**: Efficient chat monitoring with low resource usage
- **Smart Triggering**: Only processes messages that match configured triggers
- **Rate Limiting**: Built-in delays prevent spam
- **Memory Efficient**: Lightweight data storage for triggers and settings

## Compatibility

- Works with all BombSquad chat systems
- Compatible with most other chat and UI mods
- Supports both public and private servers
- Works in all game modes with chat functionality

## Important Notes

- Responses are sent from your account, so use responsibly
- Wildcard matching may trigger unexpectedly - test your triggers
- Delay timing helps prevent unnatural immediate responses
- Self-response feature can be disabled to avoid loops
- All configuration is saved automatically

## Troubleshooting

### Common Issues:
- **Responses not triggering**: Check trigger spelling and case sensitivity settings
- **Duplicate responses**: Ensure triggers aren't too broad with wildcard enabled
- **Performance issues**: Reduce number of triggers or increase delay times
- **Configuration lost**: Settings automatically save; verify file permissions

### Best Practices:
- Start with a few simple triggers
- Test triggers in different contexts
- Use appropriate delay times for natural conversation flow
- Regularly review and update your response list

## Privacy and Ethics

- Only responds to messages you explicitly configure
- No data collection or external communication
- All processing happens locally on your device
- Respect other players - use automation responsibly

## Screenshots

<img width="368" height="368" alt="Image" src="https://github.com/user-attachments/assets/f5e4ed33-eb39-47af-80b2-cba2c696b5f0" />
<img width="368" height="368" alt="Image" src="https://github.com/user-attachments/assets/7d4da7fc-6c1a-4c42-9976-0731152ad87c" />

## Credits

Created by the [BrotherBoard](https://github.com/BrotherBoard)  
Forked by [Less](https://github.com/danigomezdev)
