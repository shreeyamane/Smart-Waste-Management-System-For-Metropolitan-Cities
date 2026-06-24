
function createChart(id, type, labels, values, label) {

    new Chart(
        document.getElementById(id),
        {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: values
                }]
            }
        }
    );

}

createChart(
    "dailyChart",
    "line",
    dailyLabels,
    dailyValues,
    "Daily Waste"
);

createChart(
    "weeklyChart",
    "bar",
    weeklyLabels,
    weeklyValues,
    "Weekly Waste"
);

createChart(
    "monthlyChart",
    "bar",
    monthlyLabels,
    monthlyValues,
    "Monthly Waste"
);

createChart(
    "areaChart",
    "bar",
    areaLabels,
    areaValues,
    "Area Waste"
);

createChart(
    "fillChart",
    "pie",
    fillLabels,
    fillValues,
    "Fill Distribution"
);

createChart(
    "batteryChart",
    "pie",
    batteryLabels,
    batteryValues,
    "Battery Distribution"
);

createChart(
    "alertChart",
    "doughnut",
    alertLabels,
    alertValues,
    "Alert Distribution"
);

createChart(
    "topBinsChart",
    "bar",
    topLabels,
    topValues,
    "Fill Level"
);