"""
============================================================
LOGGER HELPER
============================================================
This module handles all logging for the Indeed scraper.
It writes logs to both console (with emojis) and a log file.

Usage:
    from utils.logger import Logger
    
    logger = Logger()
    logger.start()
    logger.log("STEP 1", "Launching browser...", "🚀")
    logger.stop()
============================================================
"""

from datetime import datetime
from pathlib import Path


class Logger:
    """
    Logger class that writes to both console and log file.
    
    Attributes:
        output_dir: Directory where log.txt will be saved
        log_file: File handle for the log file
        is_active: Whether logging is currently active
    """
    
    def __init__(self, output_dir: str = "./output"):
        """
        Initialize the logger.
        
        Args:
            output_dir: Directory path where log.txt will be created
        """
        self.output_dir = Path(output_dir)
        self.log_file = None
        self.is_active = False
        self.log_path = self.output_dir / "log.txt"
    
    def start(self, title: str = "INDEED PAGE LOADER"):
        """
        Start logging - creates/overwrites the log file.
        
        Args:
            title: Title to display in the log header
        """
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Open log file (overwrite mode)
        self.log_file = open(self.log_path, "w", encoding="utf-8")
        self.is_active = True
        
        # Write header
        run_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = [
            "=" * 60,
            f"{title}",
            f"Run started at: {run_timestamp}",
            "=" * 60,
            ""
        ]
        
        for line in header:
            self.log_file.write(line + "\n")
        self.log_file.flush()
    
    def log(self, step: str, message: str, emoji: str = "📋"):
        """
        Log a message to both console and file.
        
        Args:
            step: The step name (e.g., "STEP 1", "CONFIG", "SCREENSHOT")
            message: The message to log
            emoji: Emoji to display in console (not written to file)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Console message (with emoji)
        console_msg = f"[{timestamp}] {emoji} {step}: {message}"
        print(console_msg)
        
        # File message (without emoji for cleaner logs)
        if self.log_file and self.is_active:
            file_msg = f"[{timestamp}] {step}: {message}"
            self.log_file.write(file_msg + "\n")
            self.log_file.flush()
    
    def separator(self, char: str = "-", length: int = 60):
        """
        Print a separator line.
        
        Args:
            char: Character to use for the separator
            length: Length of the separator line
        """
        line = char * length
        print(line)
        
        if self.log_file and self.is_active:
            self.log_file.write(line + "\n")
            self.log_file.flush()
    
    def blank_line(self):
        """Print a blank line to both console and file."""
        print()
        
        if self.log_file and self.is_active:
            self.log_file.write("\n")
            self.log_file.flush()
    
    def stop(self, success: bool = True):
        """
        Stop logging and close the log file.
        
        Args:
            success: Whether the run completed successfully
        """
        if self.log_file and self.is_active:
            # Write footer
            end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "COMPLETED SUCCESSFULLY" if success else "COMPLETED WITH ERRORS"
            
            footer = [
                "",
                "=" * 60,
                f"Run {status}",
                f"Ended at: {end_timestamp}",
                "=" * 60
            ]
            
            for line in footer:
                self.log_file.write(line + "\n")
            
            self.log_file.close()
            self.log_file = None
            self.is_active = False
    
    def get_log_path(self) -> Path:
        """Return the path to the log file."""
        return self.log_path
