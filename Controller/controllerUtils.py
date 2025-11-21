from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
import math
from tkinter import filedialog
import re
import os


def sortSchedulesByTime(data):
    # Priority for the days, no classes on SAT, SUN but who knows..
    dayOrder = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4}

    def getEarliestMeeting(schedule):
        times = []
        for entry in schedule[4:]:
            try:
                day, time_range = entry.split()
                startTime = time_range.split("-")[0]
                hour, minute = map(int, startTime.split(":"))
                times.append((dayOrder[day], hour, minute))
            except Exception:
                continue
        return min(times) if times else (float("inf"), float("inf"), float("inf"))

    # sort using the funciton we give it, usingt he times
    return sorted(data, key=getEarliestMeeting)


def filterDurations(times, dur):
    valid = []
    for t in times:
        t = t.replace("^", "").strip()
        try:
            day, time_range = t.split(" ")
            start, end = time_range.split("-")

            fmt = "%H:%M"
            start_time = datetime.strptime(start, fmt)
            end_time = datetime.strptime(end, fmt)

            duration = (end_time - start_time).seconds / 60
            if duration == dur:
                valid.append(t)
        except ValueError:
            continue
    return valid


def orderedSchedules(schedules, order):
    schedules = sortSchedulesByTime(schedules)
    reoderedSchedules = []
    if not schedules:
        return schedules

    if order == "Default":
        return schedules
    else:
        result = {}
        for row in schedules:
            course, faculty, room, lab, *days = row
            if order == "Rooms & Labs":
                if room not in result:
                    result[room] = []

                result[room].append([course, faculty] + days)
            elif order == "Faculty":
                if faculty not in result:
                    result[faculty] = []

                result[faculty].append([course, room, lab] + days)

        for row in schedules:
            course, faculty, room, lab, *days = row
            if order == "Rooms & Labs":
                if lab not in (None, "None"):
                    if lab not in result:
                        result[lab] = []
                    times = filterDurations(days, 110)
                    result[lab].append([course, faculty] + times)

        reoderedSchedules.append(result)

    return reoderedSchedules


def parseMeeting(meeting):
    try:
        day, times = meeting.split()
        times = times.replace("^", "")
        startStr, endStr = times.split("-")
        fmt = "%H:%M"
        start = datetime.strptime(startStr, fmt)
        end = datetime.strptime(endStr, fmt)
        return day, start, end
    except Exception:
        return None, None, None


def getTimeRange(data):
    times = []
    time_pattern = re.compile(r"(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})")
    for _class in data:
        for item in _class:
            match = time_pattern.search(item)
            if match:
                start_h, start_m, end_h, end_m = map(int, match.groups())
                start = start_h + start_m / 60
                end = end_h + end_m / 60
                times.append((start, end))

    if not times:
        return None

    earliest_start = min(t[0] for t in times)
    latest_end = max(t[1] for t in times)
    rounded_latest_end = math.ceil(latest_end)

    return (int(earliest_start), rounded_latest_end)


def to12h(hour, minute):
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour % 12
    if display_hour == 0:
        display_hour = 12
    return f"{display_hour}:{minute:02d} {suffix}"


def drawSchedulePagePDF(canvas, data):
    room, classes = data  # data = [roomName(professor), classes]

    page_width, _ = letter
    margin_left = 60
    margin_top = 720
    day_width = 100
    hour_height = 50
    days = ["MON", "TUE", "WED", "THU", "FRI"]
    dayOrder = {d: i for i, d in enumerate(days)}
    canvasPadding = 3

    COLORLIST = [
        "#6fa8dc",
        "#93c47d",
        "#f6b26b",
        "#e06666",
        "#8e7cc3",
        "#d5b451",
        "#76a5af",
        "#c27ba0",
        "#a4c2f4",
        "#b6d7a8",
    ]

    # Time range
    startHour, endHour = getTimeRange(classes)

    # ---- Title ----
    canvas.setFont("Helvetica-Bold", 18)
    text = f"{room}"
    text_width = canvas.stringWidth(text, "Helvetica-Bold", 18)
    canvas.drawString((page_width - text_width) / 2, margin_top + 40, text)

    # ---- Day headers ----
    canvas.setFont("Helvetica-Bold", 12)
    for i, day in enumerate(days):
        x = margin_left + i * day_width
        canvas.drawString(x + day_width / 2 - 15, margin_top + 15, day)

    # ---- Grid ----
    canvas.setLineWidth(0.5)
    for hour in range(startHour, endHour + 1):
        y = margin_top - ((hour - startHour) * hour_height)

        canvas.setFont("Helvetica", 10)
        canvas.drawRightString(margin_left - 5, y, to12h(hour, 0))
        canvas.line(margin_left, y, margin_left + day_width * 5, y)

    # ---- Classes ----
    colorIndex = 0
    for cls in classes:
        course, prof, *meetings = cls

        for meeting in meetings:
            day, start, end = parseMeeting(meeting)
            if day not in dayOrder or start is None:
                continue

            color_hex = COLORLIST[colorIndex % len(COLORLIST)]
            canvas.setFillColor(colors.HexColor(color_hex))

            x = margin_left + dayOrder[day] * day_width + 2
            y = margin_top - (
                (start.hour + start.minute / 60 - startHour) * hour_height
            )
            height = ((end - start).seconds / 3600) * hour_height - 2

            # block
            canvas.rect(x, y - height, day_width - 4, height, fill=1, stroke=0)

            # text
            canvas.setFillColor(colors.white)
            canvas.setFont("Helvetica", 9)
            block_text = f"{course}\n{prof}\n{to12h(start.hour, start.minute)} - {to12h(end.hour, end.minute)}"

            text_x = x + (day_width - 4) / 2
            text_y = y - height / 2 - canvasPadding

            for idx, line in enumerate(block_text.split("\n")):
                canvas.drawCentredString(text_x, text_y + (idx * 10) - 10, line)

        colorIndex += 1


def exportOneSchedulePDF(room_classes, output_dir):
    room, classes = room_classes  # room_classes = [roomName(proffessro name), classes]
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{room}_schedule.pdf"

    # Canvas name does not work.... Don't do that pleae
    can = canvas.Canvas(filename, pagesize=letter)

    drawSchedulePagePDF(can, room_classes)

    # Save the PDF
    can.save()
    print(f"PDF saved: {filename}")


def exportMultiPagePDF(schedule, output_dir, filename):
    filename = os.path.join(output_dir, filename)
    order_ways = ["Rooms & Labs", "Faculty"]
    can = canvas.Canvas(filename, pagesize=letter)
    # Little messy :(
    for order in order_ways:
        orderedSch = orderedSchedules(schedule, order)
        for i, ele in enumerate(orderedSch):
            for name, sch in ele.items():
                drawSchedulePagePDF(can, [name, sch])
                # Only start a new page if not last page

                can.showPage()

    can.save()
    print(f"Multi-page PDF saved: {filename}")


def drawScheduleSVG(room_classes):
    name, classes = room_classes

    days = ["MON", "TUE", "WED", "THU", "FRI"]
    day_positions = {d: i for i, d in enumerate(days)}

    startHour, endHour = getTimeRange(classes)

    left_margin = 55
    day_width = 125
    hour_height = 60

    svg_width = left_margin + day_width * 5 + 20
    svg_height = (endHour - startHour) * hour_height + 80

    svg = f"<h2>{name}</h2>"
    svg += f'<svg width="{svg_width}" height="{svg_height}">\n'
    for i, day in enumerate(days):
        x = left_margin + i * day_width + day_width / 2
        svg += f'<text x="{x}" y="20" text-anchor="middle" font-size="13" font-weight="700">{day}</text>\n'

    for h in range(startHour, endHour + 1):
        y = 40 + (h - startHour) * hour_height
        svg += f'<line x1="{left_margin}" y1="{y}" x2="{svg_width}" y2="{y}" stroke="#ccc" stroke-width="1" />\n'
        svg += f'<text x="5" y="{y + 5}" font-size="11">{to12h(h, 0)}</text>\n'

    # Colors
    COLORLIST = [
        "#6fa8dc",
        "#93c47d",
        "#f6b26b",
        "#e06666",
        "#8e7cc3",
        "#d5b451",
        "#76a5af",
        "#c27ba0",
        "#a4c2f4",
        "#b6d7a8",
    ]
    color_index = 0

    for cls in classes:
        course, prof, *meetings = cls
        color = COLORLIST[color_index % len(COLORLIST)]

        for meeting in meetings:
            day, start, end = parseMeeting(meeting)
            if day not in day_positions:
                continue

            x = left_margin + day_positions[day] * day_width + 2
            y = 40 + ((start.hour + start.minute / 60 - startHour) * hour_height)
            height = ((end - start).seconds / 3600) * hour_height

            svg += f'<rect x="{x}" y="{y}" width="{day_width - 4}" height="{height}" fill="{color}" stroke="none" />\n'

            svg += f'<text x="{x + 8}" y="{y + 15}" font-size="11" font-weight="700">{to12h(start.hour, start.minute)} - {to12h(end.hour, end.minute)}</text>\n'
            svg += f'<text x="{x + 8}" y="{y + 30}" font-size="11">{prof}</text>\n'
            svg += f'<text x="{x + 8}" y="{y + 45}" font-size="11">{course}</text>\n'

        color_index += 1

    svg += "</svg>"
    return svg


def exportOneScheduleHTML(room_classes, dir):
    room, classes = room_classes
    os.makedirs(dir, exist_ok=True)
    filename = f"{dir}/{room}_schedule.html"
    html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>{room} Weekly Schedule</title>

        <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f0f0f0;
        }}
        .severator {{
            margin: auto;
            height:10px ;
            width: 100%;
            background: #f0f0f0;
        }}
        .schedule-container {{
            background: white;
            width: 700px;
            margin: 20px auto;
            padding: 10px;

        }}
        h2 {{
            text-align: center;
            margin: 0 0 10px 0;
        }}
        text {{
            font-family: Arial, sans-serif;
        }}
        </style>

        </head>
        <body>
        <div class="schedule-container">
    """

    html += drawScheduleSVG(room_classes)

    html += "</div></body></html>"

    with open(filename, "w") as f:
        f.write(html)

    print("Saved:", filename)


def exportMultiScheduleHTML(schedules, filepath):
    titel = filepath[:-5].split("/")[-1]
    order_ways = ["Rooms & Labs", "Faculty"]

    html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>{titel} Weekly Schedule</title>

    <style>
    body {{
        font-family: Arial, sans-serif;
        background: #f0f0f0;
    }}
    .schedule-container {{
        background: white;
        width: 700px;
        margin: 20px auto;
        padding: 10px;
    }}
    #nav-bar {{
        text-align: center;
        margin-bottom: 20px;
        font-size: 18px;
    }}
    #nav-bar button {{
        padding: 6px 12px;
        margin: 0px 10px;
    }}

    .single-svg {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        text-align: center;
        margin-bottom: 20px;
    }}

    .svg-page {{
        display: none;
    }}

    @media print {{
        .single-svg {{
            display: flex;
            flex-direction: column;
            align-items: center;
            page-break-after: always;
        }}

        #nav-bar {{
            display: none;
        }}
    }}

    .seperator {{
        margin: auto;
        height:10px;
        width: 100%;
        background: #f0f0f0;
    }}
    </style>

    </head>
    <body>

    <div class="schedule-container">

    <div id="nav-bar">
        <button id="leftbutton">Previous</button>
        <span id="num">1 of 1</span>
        <button id="rightbutton">Next</button>
    </div>

    <div id="svg-container">
    """

    page_number = 1

    for sch in schedules:
        page_html_parts = []

        for order in order_ways:
            orderedSch = orderedSchedules(sch, order)
            for ele in orderedSch:
                for name, sche in ele.items():
                    svg = drawScheduleSVG([name, sche])
                    page_html_parts.append(f'<div class="single-svg">{svg}</div>')

        page_content = ('\n<div class="seperator"></div>\n').join(page_html_parts)

        html += f'<div class="svg-page" id="p{page_number}">\n{page_content}\n</div>\n'

        page_number += 1

    max_pages = page_number - 1

    html += f"""
    </div>  <!-- svg-container -->
    </div>  <!-- schedule-container -->

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>

    <script>
    let maxPages = {max_pages};

    $(document).ready(function () {{
        $(".svg-page").hide();
        $("#p1").show();
        $("#num").text("1 of " + maxPages);

        $("#leftbutton").click(function () {{
            let num = parseInt($("#num").text());
            if (num > 1) {{
                num -= 1;
                $("#num").text(num + " of " + maxPages);
                $(".svg-page").hide();
                $("#p" + num).show();
            }}
        }});

        $("#rightbutton").click(function () {{
            let num = parseInt($("#num").text());
            if (num < maxPages) {{
                num += 1;
                $("#num").text(num + " of " + maxPages);
                $(".svg-page").hide();
                $("#p" + num).show();
            }}
        }});
    }});
    </script>

    </body>
    </html>
    """

    with open(filepath, "w") as f:
        f.write(html)

    print("Saved:", filepath)


def exportSchedulesBTN(data, pathEntaryVar):
    filePath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[
            ("JSON files", "*.json"),
            ("PDF files", "*.pdf"),
            ("HTML files", "*.html"),
        ],
    )

    if not filePath:
        return

    filePathSaved = filePath
    ext = filePathSaved.lower().split(".")[-1]

    if ext == "json":
        import json

        with open(filePathSaved, "w") as f:
            json.dump(data, f, indent=4)

    elif ext == "pdf":
        # directory with same base name
        output_dir = filePathSaved[:-4]
        os.makedirs(output_dir, exist_ok=True)

        for i, schedule_dict in enumerate(data):
            filename = f"Schedule_{i + 1}.pdf"
            exportMultiPagePDF(schedule_dict, output_dir, filename)

    elif ext == "html":
        # exportMultiScheduleHTML(data, filePath)
        exportMultiScheduleHTML(data, filePathSaved)

    else:
        pathEntaryVar.set("Unsupported file type selected!")
        return

    pathEntaryVar.set(f"Schedules have been saved to: {filePath}")
    # pathEntaryVar.set(f"Schedules saved to: {filePath}")
