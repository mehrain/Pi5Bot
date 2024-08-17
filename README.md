# Pi5Bot
A personal discord bot running on my raspberrypi. Ships with ready to use docker image in case you want to give it a whirl aswell.

## Features
- [x] **Runs a SQLite Database**: Utilizes a SQLite database to efficiently store and manage the list of archmages and their respective Pokémon. This ensures data persistence and quick access to the stored information.
- [x] **Match Archmages with Pokémon**: Provides functionality to match archmages with their respective Pokémon. This feature ensures that each archmage is correctly associated with their Pokémon, facilitating easy retrieval and display of this information.
- [x] **Automatic Updates**: Automatically updates the list of archmages and their Pokémon every 15 minutes (or any other specified time interval). This feature ensures that the data remains current and accurate without requiring manual intervention.
- [x] **User-Friendly Interface**: Offers a user-friendly interface for interacting with the database and viewing the list of archmages and their Pokémon. This makes it easy for users to navigate and utilize the application.
- [x] **Customizable Update Intervals**: Allows users to customize the time interval for automatic updates. Users can set the update frequency according to their preferences or requirements.
- [x] **Error Handling and Logging**: Implements robust error handling and logging mechanisms to ensure smooth operation and easy troubleshooting. This helps in maintaining the reliability and stability of the application.
- [x] **Scalability**: Designed to handle a growing list of archmages and Pokémon, ensuring that the application remains performant and responsive as the dataset expands.
- [x] **Cross-Platform Compatibility**: Ensures compatibility across different platforms, allowing users to run the application on various operating systems without any issues.

## Notes
- **a .env file is required to run the bot. This .env should be placed in the root directory of this project. The .env file should contain the following:** 
-- DISCORD_TOKEN=your_discord_token
