from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QListWidget, QListWidgetItem
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from api import upload_csv, load_history, save_history
from datetime import datetime
import numbers


class Upload(QWidget):
    def __init__(self, token, on_logout):
        super().__init__()
        self.token = token
        self.on_logout = on_logout

        self.history = load_history()
        self.current = None

        layout = QVBoxLayout()

        upload_btn = QPushButton("Upload CSV")
        upload_btn.clicked.connect(self.handle_upload)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.on_logout)

        # Summary
        self.summary_label = QLabel("Summary")
        self.summary_content = QLabel("")
        self.summary_content.setWordWrap(True)

        # History list
        self.history_label = QLabel("Recent Uploads")
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.select_history_item)

        # Plot
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(upload_btn)
        layout.addWidget(logout_btn)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.summary_content)
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_list)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.refresh_history_ui()

    # ---------- Upload ----------
    def handle_upload(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if not path:
            return

        res = upload_csv(self.token, path)
        data = res.json()

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data,
        }

        self.current = entry
        self.history = [entry] + self.history[:4]

        save_history(self.history)
        self.refresh_history_ui()
        self.render(entry)

    # ---------- History ----------
    def refresh_history_ui(self):
        self.history_list.clear()
        for item in self.history:
            lw_item = QListWidgetItem(item["timestamp"])
            self.history_list.addItem(lw_item)

    def select_history_item(self, item):
        idx = self.history_list.row(item)
        entry = self.history[idx]
        self.current = entry
        self.render(entry)

    # ---------- Rendering ----------
    def render(self, entry):
        self.render_summary(entry["data"])
        self.render_chart(entry["data"])

    def render_summary(self, data):
        lines = []
        for k, v in data.items():
            if isinstance(v, (int, float, str)):
                label = k.replace("_", " ").title()
                lines.append(f"{label}: {v}")
        self.summary_content.setText("\n".join(lines))

    def render_chart(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        dist = data.get("equipment_type_distribution")
        if not dist:
            ax.text(0.5, 0.5, "No distribution data",
                    ha="center", va="center")
            ax.axis("off")
            self.canvas.draw()
            return

        labels = list(dist.keys())
        values = list(dist.values())
        x = range(len(labels))

        ax.bar(x, values)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_title("Equipment Type Distribution")
        ax.set_ylabel("Count")

        self.figure.tight_layout()
        self.canvas.draw()
