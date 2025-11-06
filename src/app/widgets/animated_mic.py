from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRectF, pyqtProperty, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
import qtawesome as qta
import math

# Color system for different states
COLORS = {
    'ready': '#808080',      # Gray
    'listening': '#4CAF50',  # Green
    'processing': '#FFC107', # Yellow/Amber
    'error': '#F44336',      # Red
    'speaking': '#2196F3'    # Blue
}

class AnimatedMicrophoneIcon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(120, 120)
        self.setMaximumSize(200, 200)
        
        # Animation state
        self._pulse_scale = 1.0
        self._current_state = 'ready'
        self._audio_level = 0.0
        self._wave_offset = 0.0
        
        # Animation timer for waveform
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_wave)
        
        # Pulse animation
        self.pulse_animation = QPropertyAnimation(self, b"pulse_scale")
        self.pulse_animation.setDuration(1000)  # 1 second pulse
        self.pulse_animation.setStartValue(1.0)
        self.pulse_animation.setEndValue(1.2)
        self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.pulse_animation.setLoopCount(-1)  # Loop forever
        
        # Microphone icon
        self.mic_icon = qta.icon('fa5s.microphone', color='white')
        
    @pyqtProperty(float)
    def pulse_scale(self):
        return self._pulse_scale
    
    @pulse_scale.setter
    def pulse_scale(self, value):
        self._pulse_scale = value
        self.update()
    
    def set_state(self, state):
        """Set the current state (ready, listening, processing, error, speaking)"""
        if state in COLORS:
            self._current_state = state
            
            if state == 'listening':
                self.start_animation()
            else:
                self.stop_animation()
            
            self.update()
    
    def set_audio_level(self, level):
        """Update audio level (0.0 to 1.0)"""
        self._audio_level = max(0.0, min(1.0, level))
        self.update()
    
    def start_animation(self):
        """Start pulsing and waveform animations"""
        if not self.pulse_animation.state() == QPropertyAnimation.State.Running:
            self.pulse_animation.start()
        if not self.animation_timer.isActive():
            self.animation_timer.start(16)  # ~60 FPS
    
    def stop_animation(self):
        """Stop animations"""
        if self.pulse_animation.state() == QPropertyAnimation.State.Running:
            self.pulse_animation.stop()
        if self.animation_timer.isActive():
            self.animation_timer.stop()
        self._pulse_scale = 1.0
        self._wave_offset = 0.0
        self.update()
    
    def _update_wave(self):
        """Update waveform animation offset"""
        self._wave_offset += 0.1
        if self._wave_offset > 2 * math.pi:
            self._wave_offset = 0.0
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        base_radius = min(width, height) / 3
        
        # Get current color
        color = QColor(COLORS[self._current_state])
        
        # Draw waveform rings (only when listening and audio detected)
        if self._current_state == 'listening' and self._audio_level > 0.05:
            num_rings = 3
            for i in range(num_rings):
                # Calculate ring properties
                ring_progress = (self._wave_offset + i * 0.7) % (2 * math.pi)
                ring_radius = base_radius + (ring_progress / (2 * math.pi)) * base_radius * 1.5
                
                # Opacity decreases as ring expands
                opacity = int(255 * (1 - ring_progress / (2 * math.pi)) * self._audio_level)
                ring_color = QColor(color)
                ring_color.setAlpha(max(0, min(255, opacity)))
                
                # Draw ring
                pen = QPen(ring_color)
                pen.setWidth(3)
                painter.setPen(pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawEllipse(
                    QRectF(
                        center_x - ring_radius,
                        center_y - ring_radius,
                        ring_radius * 2,
                        ring_radius * 2
                    )
                )
        
        # Draw main circle (background)
        painter.setPen(Qt.PenStyle.NoPen)
        bg_color = QColor(color)
        bg_color.setAlpha(40)
        painter.setBrush(bg_color)
        scaled_radius = base_radius * self._pulse_scale
        painter.drawEllipse(
            QRectF(
                center_x - scaled_radius,
                center_y - scaled_radius,
                scaled_radius * 2,
                scaled_radius * 2
            )
        )
        
        # Draw border circle
        border_pen = QPen(color)
        border_pen.setWidth(3)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(
            QRectF(
                center_x - scaled_radius,
                center_y - scaled_radius,
                scaled_radius * 2,
                scaled_radius * 2
            )
        )
        
        # Draw microphone icon in center
        icon_size = int(base_radius * 0.8)
        icon_rect = QRectF(
            center_x - icon_size / 2,
            center_y - icon_size / 2,
            icon_size,
            icon_size
        )
        self.mic_icon.paint(painter, icon_rect.toRect())
        
        # Draw state text below
        painter.setPen(QPen(color))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        
        state_text = self._current_state.capitalize()
        text_rect = QRectF(0, height - 25, width, 25)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, state_text)



