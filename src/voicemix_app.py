"""
VoiceMix - Main GUI Application
Desktop application for MP3 voice processing with PyQt6
"""

import sys
import os
import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QFileDialog, QMessageBox,
    QTextEdit, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont, QIcon, QPalette, QColor

from audio_processor import AudioProcessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voicemix.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProcessingThread(QThread):
    """Worker thread for audio processing"""
    
    progress_update = pyqtSignal(int, str)
    processing_complete = pyqtSignal(bool, str)
    
    def __init__(self, input_file: str, output_file: str):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.processor = AudioProcessor()
    
    def run(self):
        """Run audio processing in background thread"""
        try:
            logger.info(f"Processing thread started for: {self.input_file}")
            
            success = self.processor.process_audio_file(
                self.input_file,
                self.output_file,
                progress_callback=self._progress_callback
            )
            
            if success:
                self.processing_complete.emit(True, self.output_file)
            else:
                self.processing_complete.emit(False, "Processing failed")
                
        except Exception as e:
            logger.error(f"Error in processing thread: {e}", exc_info=True)
            self.processing_complete.emit(False, str(e))
        finally:
            self.processor.cleanup()
    
    def _progress_callback(self, progress: int, message: str):
        """Callback for progress updates"""
        self.progress_update.emit(progress, message)


class DropZoneLabel(QLabel):
    """Custom label widget that accepts drag and drop"""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setMinimumHeight(150)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f5f5f5;
                padding: 20px;
                font-size: 14px;
                color: #666;
            }
            QLabel:hover {
                border-color: #2196F3;
                background-color: #e3f2fd;
                color: #1976D2;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1 and urls[0].toLocalFile().lower().endswith('.mp3'):
                event.acceptProposedAction()
                self.setStyleSheet("""
                    QLabel {
                        border: 2px dashed #4CAF50;
                        border-radius: 10px;
                        background-color: #e8f5e9;
                        padding: 20px;
                        font-size: 14px;
                        color: #2E7D32;
                    }
                """)
    
    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f5f5f5;
                padding: 20px;
                font-size: 14px;
                color: #666;
            }
            QLabel:hover {
                border-color: #2196F3;
                background-color: #e3f2fd;
                color: #1976D2;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        urls = event.mimeData().urls()
        if len(urls) == 1:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith('.mp3'):
                self.file_dropped.emit(file_path)
                event.acceptProposedAction()
        
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f5f5f5;
                padding: 20px;
                font-size: 14px;
                color: #666;
            }
            QLabel:hover {
                border-color: #2196F3;
                background-color: #e3f2fd;
                color: #1976D2;
            }
        """)


class VoiceMixApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.output_file = None
        self.processing_thread = None
        
        self.init_ui()
        logger.info("VoiceMix application initialized")
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("VoiceMix - MP3 Voice Processor")
        self.setMinimumSize(700, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("VoiceMix")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #1976D2; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Convert multiple voices in MP3 files to a unified voice")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)
        
        # File input section
        input_group = QGroupBox("1. Select MP3 File")
        input_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 10px; }")
        input_layout = QVBoxLayout()
        
        # Drag and drop zone
        self.drop_zone = DropZoneLabel(
            "Drag & Drop MP3 file here\nor\nClick 'Browse' to select file"
        )
        self.drop_zone.file_dropped.connect(self.on_file_dropped)
        input_layout.addWidget(self.drop_zone)
        
        # Browse button
        self.browse_btn = QPushButton("📁 Browse Files")
        self.browse_btn.clicked.connect(self.browse_file)
        self.browse_btn.setMinimumHeight(40)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        input_layout.addWidget(self.browse_btn)
        
        # Selected file label
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #666; font-style: italic; margin-top: 10px;")
        self.file_label.setWordWrap(True)
        input_layout.addWidget(self.file_label)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Processing section
        processing_group = QGroupBox("2. Process Audio")
        processing_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 10px; }")
        processing_layout = QVBoxLayout()
        
        # Process button
        self.process_btn = QPushButton("🎵 Start Processing")
        self.process_btn.clicked.connect(self.start_processing)
        self.process_btn.setEnabled(False)
        self.process_btn.setMinimumHeight(50)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)
        processing_layout.addWidget(self.process_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ccc;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        processing_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to process")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666; margin-top: 5px;")
        processing_layout.addWidget(self.status_label)
        
        processing_group.setLayout(processing_layout)
        main_layout.addWidget(processing_group)
        
        # Output section
        output_group = QGroupBox("3. Download Result")
        output_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 10px; }")
        output_layout = QVBoxLayout()
        
        # Download button
        self.download_btn = QPushButton("💾 Save Processed File")
        self.download_btn.clicked.connect(self.save_output)
        self.download_btn.setEnabled(False)
        self.download_btn.setMinimumHeight(40)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)
        output_layout.addWidget(self.download_btn)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QGroupBox {
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                color: #333;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
    
    def browse_file(self):
        """Open file browser to select MP3 file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select MP3 File",
            "",
            "MP3 Files (*.mp3);;All Files (*)"
        )
        
        if file_path:
            self.on_file_dropped(file_path)
    
    def on_file_dropped(self, file_path: str):
        """Handle file selection (drop or browse)"""
        if not file_path.lower().endswith('.mp3'):
            QMessageBox.warning(
                self,
                "Invalid File",
                "Please select a valid MP3 file."
            )
            return
        
        if not os.path.exists(file_path):
            QMessageBox.warning(
                self,
                "File Not Found",
                "The selected file does not exist."
            )
            return
        
        self.input_file = file_path
        self.file_label.setText(f"Selected: {os.path.basename(file_path)}")
        self.file_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        self.process_btn.setEnabled(True)
        self.download_btn.setEnabled(False)
        self.output_file = None
        
        logger.info(f"File selected: {file_path}")
    
    def start_processing(self):
        """Start audio processing"""
        if not self.input_file:
            return
        
        # Create output file path
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        input_name = Path(self.input_file).stem
        self.output_file = str(output_dir / f"{input_name}_unified.mp3")
        
        # Disable controls
        self.process_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.drop_zone.setAcceptDrops(False)
        
        # Reset progress
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting processing...")
        
        # Start processing thread
        self.processing_thread = ProcessingThread(self.input_file, self.output_file)
        self.processing_thread.progress_update.connect(self.on_progress_update)
        self.processing_thread.processing_complete.connect(self.on_processing_complete)
        self.processing_thread.start()
        
        logger.info("Processing started")
    
    def on_progress_update(self, progress: int, message: str):
        """Handle progress updates from processing thread"""
        if progress >= 0:
            self.progress_bar.setValue(progress)
        self.status_label.setText(message)
    
    def on_processing_complete(self, success: bool, message: str):
        """Handle processing completion"""
        # Re-enable controls
        self.browse_btn.setEnabled(True)
        self.drop_zone.setAcceptDrops(True)
        
        if success:
            self.progress_bar.setValue(100)
            self.status_label.setText("Processing completed successfully!")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.download_btn.setEnabled(True)
            
            QMessageBox.information(
                self,
                "Success",
                "Audio processing completed successfully!\n\n"
                "Click 'Save Processed File' to download the result."
            )
            
            logger.info("Processing completed successfully")
        else:
            self.status_label.setText(f"Processing failed: {message}")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
            self.process_btn.setEnabled(True)
            
            QMessageBox.critical(
                self,
                "Processing Failed",
                f"An error occurred during processing:\n\n{message}"
            )
            
            logger.error(f"Processing failed: {message}")
    
    def save_output(self):
        """Save the processed audio file"""
        if not self.output_file or not os.path.exists(self.output_file):
            QMessageBox.warning(
                self,
                "No Output File",
                "No processed file available to save."
            )
            return
        
        # Ask user where to save
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Processed Audio",
            os.path.basename(self.output_file),
            "MP3 Files (*.mp3);;All Files (*)"
        )
        
        if save_path:
            try:
                # Copy file to selected location
                import shutil
                shutil.copy2(self.output_file, save_path)
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"File saved successfully to:\n{save_path}"
                )
                
                logger.info(f"Output file saved to: {save_path}")
                
                # Reset for new processing
                self.process_btn.setEnabled(True)
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Save Failed",
                    f"Failed to save file:\n{str(e)}"
                )
                logger.error(f"Failed to save file: {e}")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application info
    app.setApplicationName("VoiceMix")
    app.setOrganizationName("VoiceMix")
    
    window = VoiceMixApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
