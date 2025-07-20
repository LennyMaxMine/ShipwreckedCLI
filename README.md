# ShipwreckedCli

A powerful terminal-based client for Hack Club's Shipwrecked hackathon website, built with Python to provide nearly complete functionality equivalent to the web interface.

<div align="center">
  <a href="https://shipwrecked.hackclub.com/?t=ghrm" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/739361f1d440b17fc9e2f74e49fc185d86cbec14_badge.png" 
         alt="This project is part of Shipwrecked, the world's first hackathon on an island!" 
         style="width: 35%;">
  </a>
</div>

## Features

- **Complete Account Management**: View and manage your Shipwrecked profile
- **Progress Tracking**: Monitor your journey to the island
- **Shop Integration**: Browse items, place orders, and manage inventory
- **Leaderboard Access**: Check rankings and competition stats
- **Session Management**: Handle authentication and user sessions
- **Interactive CLI**: User-friendly command-line interface with help system

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LennyMaxMine/shipwreckedcli
   cd ShipwreckedCli
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### General Commands

| Command | Description |
|---------|-------------|
| `help` | Show the main help message |
| `whoami` | Display your user profile data |
| `session` | Show current session information |
| `progress` | View your progress toward the island |
| `leaderboard <length>` | Display leaderboard sorted by hours |
| `logut` | Delete all your locally stored account data  |

### Shop Commands

Access the shop with the `shop` command, then use:

| Command | Description |
|---------|-------------|
| `items` | Browse available shop items |
| `purchase <item>` | Buy a shop item *(under development)* |
| `orders` | View your order history |
| `inventory` | Check your fulfilled orders |
| `back` | Return to main menu |

### User Management Commands

Access user settings with the `user` command, then use:

| Command | Description |
|---------|-------------|
| `name` | Display your name |
| `email` | Show your email address |
| `address` | View your address |
| `birthday` | Display your birthday |
| `phone` | Show your phone number |
| `id` | Print your user ID |
| `email-verification` | Check email verification status |
| `identity-verification` | Check identity verification status |
| `slack-connected` | Show Slack connection status |
| `back` | Return to main menu |

### Always Available Commands
| Command | Description |
|---------|-------------|
| `exit` | Exit the application |
| `clear` | Clear the screen |

### Getting Help

- Use `help` for general commands
- Use `help <submenu>` (e.g., `help shop`) for submenu-specific commands
- Commands are available context-sensitively based on your current menu

## Development Status

This project is actively developed for the 2025 Hack Club Shipwrecked Hackathon. Some features like shop purchases are still under construction.

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`
- Valid Shipwrecked account credentials

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file (which will be added later :D) for details.

## Credits

Developed with ♥ by **LennyMaxMine** in Frankfurt, Germany for the 2025 Hack Club Shipwrecked Hackathon.

---

###  This Project is not officially from Hack Club. It is made by a member of Hack Club.

