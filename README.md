# Illustration Gallery

This application is designed to manage an gallery of illustrations with features such as progress checklists and social media tracking. It's also designed with images first, so that files or folders without descriptive names don't get in the way of the you getting to your images as quickly as possible.

## Features

- **Gallery View**: Display illustrations with relevant details such as title, last edited date, and progress status.
- **Progress Checklists**: Track the progress of each illustration with a dedicated checklist. (WIP)
- **Social Media Tracking**: Manage and format social media posts for each illustration. (WIP)


## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd illustration-gallery
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Project Structure

```
illustration-gallery
├── src
│   ├── main.py
│   ├── gui
│   │   ├── app_window.py
│   │   └── components
│   │       ├── checklist.py
│   │       ├── social_media_tracker.py
│   │       └── gallery_view.py
│   ├── models
│   │   ├── illustration.py
│   │   └── user_data.py
│   ├── services
│   │   ├── data_manager.py
│   │   └── social_media_service.py
│   └── utils
│       └── helpers.py
├── requirements.txt
└── README.md
```

## Contributing

Need a niche usecase that would benefit your usage of this? Fork and edit your heart away!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.