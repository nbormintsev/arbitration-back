def devices_to_dict(devices: list) -> dict[int, dict]:
    return {
        row['id']: {
            k: v for k, v in row.items() if k != 'id'
        } for row in devices
    }
