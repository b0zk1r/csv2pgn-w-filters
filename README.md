# CSV to PGN Database Converter

A user-friendly Windows application to convert chess games from CSV format to PGN format with filtering capabilities.

![Application Screenshot](screenshot.png)

## Features

- Convert CSV files containing chess games to PGN format
- Filter games by:
  - Rating range
  - Chess openings
  - Puzzle themes
- Preview CSV data before conversion
- User-friendly GUI interface
- Progress tracking during conversion
- Detailed logging

## Installation

1. Download the latest release from the [Releases](https://github.com/yourusername/cvs-to-pgn-w-filters/releases) page
2. Extract the ZIP file
3. Run `CSVtoPGNConverter.exe`

## Usage

1. Click "Browse" to select your input CSV file
2. Click "Browse" to choose where to save the output PGN file
3. (Optional) Set filters:
   - Adjust rating range
   - Select openings
   - Select themes
4. Click "Preview Data" to see the contents of your CSV file
5. Click "Convert" to start the conversion process
6. Monitor progress in the log window
7. When complete, your PGN file will be saved at the specified location

## CSV File Format

Your CSV file should contain at least one of these columns for moves:
- moves
- pgn
- game_moves
- notation

And at least one of these columns for ratings:
- rating
- white_rating
- black_rating
- player_rating

## License

MIT License 