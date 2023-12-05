
const studentMarks = [
    { name: 'Alice', marks: 85 },
    { name: 'Bob', marks: 78 },
    { name: 'Charlie', marks: 92 },
    { name: 'David', marks: 65 },
    { name: 'Emma', marks: 89 },
    { name: 'Frank', marks: 72 },
    { name: 'Grace', marks: 94 },
    { name: 'Henry', marks: 60 },
    { name: 'Ivy', marks: 87 },
    { name: 'Jack', marks: 76 },
    { name: 'Karen', marks: 91 },
    { name: 'Liam', marks: 82 },
    { name: 'Mia', marks: 79 },
    { name: 'Noah', marks: 88 },
    { name: 'Olivia', marks: 70 },
    { name: 'Parker', marks: 93 },
    { name: 'Quinn', marks: 68 },
    { name: 'Ryan', marks: 83 },
    { name: 'Sophia', marks: 75 },
    { name: 'Thomas', marks: 97 },
    { name: 'Uma', marks: 69 },
    { name: 'Vincent', marks: 80 },
    { name: 'Willow', marks: 84 },
    { name: 'Xavier', marks: 73 },
    { name: 'Yara', marks: 96 },
    { name: 'Zane', marks: 71 },
    { name: 'Eva', marks: 74 },
    { name: 'Logan', marks: 98 },
    { name: 'Ava', marks: 81 },
    { name: 'Owen', marks: 77 },
];

var students = studentMarks.map(student => student.name);
const marks = studentMarks.map(student => student.marks);
const grade_colors = studentMarks.map(student => {
    const marks = student.marks;
    if (marks >= 91) {
        return '#4CAF50'; // Green for 91-100
    } else if (marks >= 81) {
        return '#2196F3'; // Blue for 81-90
    } else if (marks >= 71) {
        return '#FFC107'; // Amber for 71-80
    } else if (marks >= 61) {
        return '#FF5722'; // Deep Orange for 61-70
    } else {
        return '#F44336'; // Red for 51-60 and below
    }
});

const barChartOptions = {
    series: [
        {
            name: 'Percentage',
            data: marks,
        },
    ],
    chart: {
        type: 'bar',
        height: 420,
        toolbar: {
            show: true,
        },
    },
    colors: grade_colors,
    plotOptions: {
        bar: {
            distributed: true,
            borderRadius: 5,
            horizontal: false,
            columnWidth: '60%',
            dataLabels: {
                position: 'top', // top, center, bottom
            },
        },
    },
    dataLabels: {
        enabled: true,
        formatter: function (value) {
            return value + "%";
        },
        offsetY: -20,
        style: {
            fontSize: '12px',
            colors: ["#304758"]
        }
    },
    legend: {
        show: false,
    },
    xaxis: {
        categories: students,
    },
    yaxis: {
        title: {
            text: 'Marks(%)',
        },
    }
};

const barChart = new ApexCharts(
    document.querySelector('#bar-chart'),
    barChartOptions
);
barChart.render();

function categorizeMarks(marks) {
    if (marks >= 90) return '90+';
    if (marks >= 80) return '80-89';
    if (marks >= 70) return '70-79';
    if (marks >= 60) return '60-69';
    return '50-59';
}

const marksCount = {
    '90+': 0,
    '80-89': 0,
    '70-79': 0,
    '60-69': 0,
    '50-59': 0,
};

studentMarks.forEach((student) => {
    const category = categorizeMarks(student.marks);
    marksCount[category]++;
});


const seriesData = Object.values(marksCount);

var options = {
    series: seriesData,
    chart: {
        type: 'donut',
    },
    labels: Object.keys(marksCount),
    responsive: [
        {
            breakpoint: 480,
            options: {
                chart: {
                    width: 200,
                },
                legend: {
                    position: 'bottom',
                },
            },
        },
    ],
};
var chart = new ApexCharts(document.querySelector("#pie-chart"), options);
var chart2 = new ApexCharts(document.querySelector("#pie-chart2"), options);
chart.render();
chart2.render();


// const areaChartOptions = {
//     series: [
//         {
//             name: 'Purchase Orders',
//             data: [31, 40, 28, 51, 42, 109, 100],
//         },
//         {
//             name: 'Sales Orders',
//             data: [11, 32, 45, 32, 34, 52, 41],
//         },
//     ],
//     chart: {
//         height: 350,
//         type: 'area',
//         toolbar: {
//             show: false,
//         },
//     },
//     colors: ['#4f35a1', '#246dec'],
//     dataLabels: {
//         enabled: false,
//     },
//     stroke: {
//         curve: 'smooth',
//     },
//     labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
//     markers: {
//         size: 0,
//     },
//     yaxis: [
//         {
//             title: {
//                 text: 'Purchase Orders',
//             },
//         },
//         {
//             opposite: true,
//             title: {
//                 text: 'Sales Orders',
//             },
//         },
//     ],
//     tooltip: {
//         shared: true,
//         intersect: false,
//     },
// };

// const areaChart = new ApexCharts(
//     document.querySelector('#area-chart'),
//     areaChartOptions
// );
// areaChart.render();