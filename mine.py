from datetime import datetime, timedelta
import uuid
import random

def uuid1_to_datetime(uuid_str):
    """Convert UUIDv1 string to datetime."""
    try:
        u = uuid.UUID(uuid_str)
        if u.version != 1:
            raise ValueError("Not a version 1 UUID.")

        # Extract time fields
        time_low = u.time_low
        time_mid = u.time_mid
        time_hi_version = u.time_hi_version & 0x0FFF  # remove version bits

        # Reconstruct 60-bit timestamp
        uuid_timestamp = (time_hi_version << 48) | (time_mid << 32) | time_low

        # Convert to datetime
        uuid_epoch = datetime(1582, 10, 15)
        delta = timedelta(microseconds=uuid_timestamp / 10)
        return uuid_epoch + delta

    except Exception as e:
        return f"Error: {e}"

def datetime_to_uuid1(input_datetime):
    """Generate UUIDv1 using a given datetime."""
    try:
        # UUID epoch
        uuid_epoch = datetime(1582, 10, 15)
        delta = input_datetime - uuid_epoch
        uuid_timestamp = int(delta.total_seconds() * 10**7)  # 100ns ticks

        # Split timestamp into UUID fields
        time_low = uuid_timestamp & 0xFFFFFFFF
        time_mid = (uuid_timestamp >> 32) & 0xFFFF
        time_hi_version = ((uuid_timestamp >> 48) & 0x0FFF) | (1 << 12)  # version 1

        # Random clock sequence
        clock_seq = random.getrandbits(14)
        clock_seq_low = clock_seq & 0xFF
        clock_seq_hi_variant = (clock_seq >> 8) & 0x3F | 0x80  # variant

        # Random node (or fixed if desired)
        node = random.getrandbits(48)

        # Pack into UUID
        return uuid.UUID(fields=(time_low, time_mid, time_hi_version,
                                 clock_seq_hi_variant, clock_seq_low, node))
    except Exception as e:
        return f"Error: {e}"

def main():
    print("UUID v1 ↔ Timestamp Tool")
    print("1. UUID → Timestamp")
    print("2. Timestamp → UUID")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        uuid_input = input("Enter UUIDv1: ").strip()
        result = uuid1_to_datetime(uuid_input)
        print("Timestamp:", result)

    elif choice == "2":
        timestamp_input = input("Enter ISO timestamp (e.g. 2025-05-20T10:15:55.200Z): ").strip()
        try:
            dt = datetime.strptime(timestamp_input, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            print("❌ Invalid timestamp format. Use ISO format like 2025-05-20T10:15:55.217Z")
            return

        result = datetime_to_uuid1(dt)
        print("Generated UUIDv1:", result)

    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
