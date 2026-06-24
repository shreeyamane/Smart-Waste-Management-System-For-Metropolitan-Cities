from app.models.alert import Alert


def create_alert(
    db,
    bin_id,
    alert_type,
    message
):

    existing = (
        db.query(Alert)
        .filter(
            Alert.bin_id == bin_id,
            Alert.alert_type == alert_type,
            Alert.status == "ACTIVE"
        )
        .first()
    )

    if existing:
        return

    alert = Alert(
        bin_id=bin_id,
        alert_type=alert_type,
        message=message,
        status="ACTIVE"
    )

    db.add(alert)