from datetime import datetime, date, timedelta
import calendar
import json

billing_month = input("Enter the month and year in mm-yyyy format: ")

month_date = datetime.strptime(billing_month, "%m-%Y")
year = month_date.year
month = month_date.month

days_in_month = calendar.monthrange(year, month)[1]
month_start = date(year, month, 1)
month_end = date(year, month, days_in_month)

billing_month = month_date.strftime("%Y-%m")
inputs = []

with open("events.csv", "r") as file:
    for line in file:
        cleaned_line = line.strip()
        inputs.append(cleaned_line.split(","))

inputs.pop(0)
prices = []

with open("plans.csv", "r") as file2:
    for line in file2:
        cleaned_line = line.strip()
        prices.append(cleaned_line.split(","))

prices.pop(0)

customers = {}

for input1 in inputs:
    customer_id = input1[0]

    if customer_id not in customers:
        customers[customer_id] = []

    customers[customer_id].append(input1)

def sort_events(record):
    return record[1]


for customer_id in customers:
    customers[customer_id].sort(key=sort_events)

def find_plan(plan_code):
    for price in prices:
        if price[0] == plan_code:
            monthly_fee = float(price[1])
            included_tokens = int(price[2])
            return monthly_fee, included_tokens

    raise ValueError(f"Plan not found: {plan_code}")

def round_fee(amount):
    amount = str(amount)
    decimal_part = amount.split(".")[1]

    if len(decimal_part) > 2 and int(decimal_part[2]) >= 5:
        amount = float(amount)
        return (int(amount * 100 + 0.5)) / 100

    return int(float(amount) * 100) / 100


def add_segment(customer_id, plan_code, active_start, segment_end):
    clipped_start = max(active_start, month_start)
    clipped_end = min(segment_end, month_end)

    if clipped_start <= clipped_end:
        monthly_fee, included_tokens = find_plan(plan_code)

        active_days = (clipped_end - clipped_start).days + 1

        fee = round_fee(
            monthly_fee * active_days / days_in_month
        )
        tokens = (
            included_tokens * active_days
        ) // days_in_month

        segments.append({
            "customer_id": customer_id,
            "plan_code": plan_code,
            "start_date": clipped_start.isoformat(),
            "end_date": clipped_end.isoformat(),
            "active_days": active_days,
            "fee": f"{fee:.2f}",
            "included_tokens": tokens
        })

segments = []

for customer_id, records in customers.items():
    active_plan = None
    active_start = None

    for record in records:
        event_date = datetime.strptime(
            record[1], "%Y-%m-%d"
        ).date()

        event_type = record[2]
        plan_code = record[3]

        if event_type == "START":
            active_plan = plan_code
            active_start = event_date

        elif event_type == "CHANGE":

            if active_plan is not None:
                segment_end = event_date - timedelta(days=1)

                add_segment(
                    customer_id,
                    active_plan,
                    active_start,
                    segment_end
                )
            active_plan = plan_code
            active_start = event_date

        elif event_type == "CANCEL":

            if active_plan is not None:
                add_segment(
                    customer_id,
                    active_plan,
                    active_start,
                    event_date
                )

            active_plan = None
            active_start = None

    if active_plan is not None:
        add_segment(
            customer_id,
            active_plan,
            active_start,
            month_end
        )

def sort_segments(segment):
    return segment["customer_id"], segment["start_date"]

segments.sort(key=sort_segments)

print("\nBilling Month:", billing_month)
print("Days in Month:", days_in_month)
print("Number of Segments:", len(segments))
print("\nSegments:")
print(json.dumps(segments, indent=4))