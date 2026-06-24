import random
import time

from app.core.database import SessionLocal

from app.models.bin import Bin
from app.models.bin_reading import BinReading
from app.models.sensor_data import SensorData
from app.models.alert import Alert

from app.services.alert_service import create_alert


class BinSimulator:

    def __init__(self):
        self.db = SessionLocal()

    def create_bins(self, count=50):

        existing = self.db.query(Bin).count()

        if existing > 0:
            print("Bins already exist")
            return

        for i in range(count):

            bin_obj = Bin(
                bin_code=f"BIN{i+1:03}",
                location=f"Location {i+1}",
                latitude=18.5204 + random.uniform(-0.05, 0.05),
                longitude=73.8567 + random.uniform(-0.05, 0.05),
                status="ACTIVE",
                fill_level=random.randint(20, 80),
                weight=round(random.uniform(1, 15), 2),
                battery=random.randint(70, 100)
            )

            self.db.add(bin_obj)

        self.db.commit()

        print(f"{count} bins created")

    def create_alert_if_needed(self, bin_obj):

        if bin_obj.fill_level > 80:

            create_alert(
                self.db,
                bin_obj.id,
                "FULL_ALERT",
                f"{bin_obj.bin_code} is above 80% ({bin_obj.fill_level}%)"
            )

        if bin_obj.fill_level > 95:

            create_alert(
                self.db,
                bin_obj.id,
                "OVERFLOW_ALERT",
                f"{bin_obj.bin_code} overflow risk ({bin_obj.fill_level}%)"
            )

        if bin_obj.battery < 20:

            create_alert(
                self.db,
                bin_obj.id,
                "MAINTENANCE_ALERT",
                f"{bin_obj.bin_code} battery low ({bin_obj.battery}%)"
            )

    def update_bins(self):

        bins = self.db.query(Bin).all()

        for b in bins:

            # Bin fill simulation

            chance = random.random()

            # 85% chance bin gets fuller
            if chance < 0.85:

                b.fill_level = min(
                    100,
                    b.fill_level + random.randint(5, 15)
                )

            # 15% chance collection happens
            else:

                b.fill_level = max(
                    0,
                    b.fill_level - random.randint(30, 80)
                )

            # Weight update

            b.weight = round(
                max(
                    0,
                    b.weight + random.uniform(-1.0, 2.0)
                ),
                2
            )

            # Battery drain

            b.battery = max(
                0,
                b.battery - random.randint(0, 1)
            )

            # Status update

            if b.fill_level >= 90:

                b.status = "FULL"

            elif b.fill_level >= 70:

                b.status = "WARNING"

            else:

                b.status = "ACTIVE"

            # Auto Resolve Alerts

            active_alerts = (
                self.db.query(Alert)
                .filter(
                    Alert.bin_id == b.id,
                    Alert.status == "ACTIVE"
                )
                .all()
            )

            for alert in active_alerts:

                if (
                    alert.alert_type == "FULL_ALERT"
                    and b.fill_level <= 80
                ):
                    alert.status = "RESOLVED"

                elif (
                    alert.alert_type == "OVERFLOW_ALERT"
                    and b.fill_level <= 95
                ):
                    alert.status = "RESOLVED"

                elif (
                    alert.alert_type == "MAINTENANCE_ALERT"
                    and b.battery >= 20
                ):
                    alert.status = "RESOLVED"

            # Reading History

            reading = BinReading(
                bin_id=b.bin_code,
                fill_level=b.fill_level,
                weight=b.weight,
                battery=b.battery
            )

            self.db.add(reading)

            # Sensor History

            sensor = SensorData(
                bin_id=b.id,
                fill_level=b.fill_level,
                temperature=round(
                    random.uniform(20, 40),
                    2
                ),
                humidity=round(
                    random.uniform(40, 90),
                    2
                )
            )

            self.db.add(sensor)

            # Alert Engine

            self.create_alert_if_needed(b)

        self.db.commit()

        print("Sensor data updated")

    def run(self):

        self.create_bins(50)

        while True:

            self.update_bins()

            time.sleep(30)