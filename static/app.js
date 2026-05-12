let selectedBuilding = "ILAB";
let chartInstance = null;
let isPredicting = false;

/* --------------------------
   BUILDING SELECTION
-------------------------- */

function setBuilding(name) {

    selectedBuilding = name;

    document.getElementById("selectedBuilding").innerText = name;
}

/* --------------------------
   INFRASTRUCTURE SIMULATION
-------------------------- */

function generateInfrastructureData() {

    return {

        transformer_load_percent:
            Math.floor(Math.random() * 100),

        grid_voltage:
            Math.floor(Math.random() * (240 - 170) + 170),

        generator_status:
            Math.random() > 0.5 ? "Active" : "Inactive",

        fuel_level_percent:
            Math.floor(Math.random() * 100),

        maintenance_status:
            ["Good", "Fair", "Poor"][
                Math.floor(Math.random() * 3)
            ],

        occupancy_level:
            ["Low", "Medium", "High"][
                Math.floor(Math.random() * 3)
            ],

        previous_outages_7days:
            Math.floor(Math.random() * 11)
    };
}

/* --------------------------
   MAIN PREDICTION
-------------------------- */

async function predict() {

    if (isPredicting) return;

    isPredicting = true;

    const btn = document.getElementById("predictBtn");

    btn.disabled = true;

    document.getElementById("statusText").innerText =
        "Refreshing live monitoring data...";

    try {

        const weather = await getWeather();

        const infra = generateInfrastructureData();

        /* UPDATE METRICS */

        document.getElementById("loadValue").innerText =
            infra.transformer_load_percent + "%";

        document.getElementById("voltageValue").innerText =
            infra.grid_voltage + "V";

        document.getElementById("weatherValue").innerText =
            weather.weather_condition;

        document.getElementById("windValue").innerText =
            weather.wind_speed_kmh.toFixed(1) + " km/h";

        /* SMALL LOADING DELAY */

        await new Promise(resolve => setTimeout(resolve, 1000));

        /* API REQUEST */

        const res = await fetch("http://127.0.0.1:8000/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                date: "2025-09-28",

                time_block: "9PM-12AM",

                building: selectedBuilding,

                weather_condition: weather.weather_condition,

                temperature_c: weather.temperature_c,

                humidity_percent: weather.humidity_percent,

                rainfall_mm: weather.rainfall_mm,

                wind_speed_kmh: weather.wind_speed_kmh,

                transformer_load_percent:
                    infra.transformer_load_percent,

                grid_voltage:
                    infra.grid_voltage,

                generator_status:
                    infra.generator_status,

                fuel_level_percent:
                    infra.fuel_level_percent,

                maintenance_status:
                    infra.maintenance_status,

                occupancy_level:
                    infra.occupancy_level,

                previous_outages_7days:
                    infra.previous_outages_7days
            })
        });

        const data = await res.json();

        /* RISK COLOR */

        let cls = "low";

        if (data.predicted_risk === "Medium")
            cls = "medium";

        if (data.predicted_risk === "High")
            cls = "high";

        if (data.predicted_risk === "Critical")
            cls = "critical";

        /* SHOW RESULT */

        document.getElementById("result").innerHTML = `
            <div class="${cls}"
                 style="
                    padding:16px;
                    border-radius:12px;
                    background:#1e293b;
                    text-align:center;
                 ">

                ${data.predicted_risk} Risk - ${data.confidence}%

            </div>
        `;

        /* DRAW CHART */

        drawChart(weather, infra);

        /* STATUS */

        document.getElementById("statusText").innerText =
            "Last Updated: " +
            new Date().toLocaleTimeString();

    }

    catch(error) {

        console.error(error);

        document.getElementById("statusText").innerText =
            "System Error, Please Refresh System";

    }

    finally {

        btn.disabled = false;

        isPredicting = false;
    }
}

/* --------------------------
   WEATHER API
-------------------------- */

async function getWeather() {



    const API_KEY = os.environ.get("WEATHER_API_KEY")


    const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=Ilorin&appid=${API_KEY}&units=metric`
    );

    const data = await response.json();

    let weatherMain = data.weather[0].main;

    if (weatherMain === "Clear") {
        weatherMain = "Sunny";
    }
    else if (weatherMain === "Clouds") {
        weatherMain = "Cloudy";
    }
    else if (weatherMain === "Rain") {
        weatherMain = "Rainy";
    }
    else if (weatherMain === "Thunderstorm") {
        weatherMain = "Stormy";
    }
    else {
        weatherMain = "Cloudy";
    }

    return {

        weather_condition: weatherMain,

        temperature_c: data.main.temp,

        humidity_percent: data.main.humidity,

        wind_speed_kmh: data.wind.speed * 3.6,

        rainfall_mm:
            data.rain ? data.rain["1h"] || 0 : 0
    };
}

/* --------------------------
   CHART
-------------------------- */

function drawChart(weather, infra) {

    if (chartInstance) {
        chartInstance.destroy();
    }

    const labels = [
        "Transformer Load",
        "Voltage Stress",
        "Humidity",
        "Wind Speed",
        "Past Outages"
    ];

    const values = [
        infra.transformer_load_percent,
        250 - infra.grid_voltage,
        weather.humidity_percent,
        weather.wind_speed_kmh,
        infra.previous_outages_7days * 10
    ];

    chartInstance = new Chart(

        document.getElementById("chart"),

        {

            type: "bar",

            data: {

                labels: labels,

                datasets: [{

                    label: "Infrastructure Stress Indicators",

                    data: values,

                    backgroundColor: [
                        "#3b82f6",
                        "#ef4444",
                        "#eab308",
                        "#06b6d4",
                        "#f97316"
                    ],

                    borderRadius: 10
                }]
            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        labels: {
                            color: "white"
                        }
                    }
                },

                scales: {

                    x: {

                        ticks: {
                            color: "white"
                        }
                    },

                    y: {

                        beginAtZero: true,

                        ticks: {
                            color: "white"
                        }
                    }
                }
            }
        }
    );
}

/* --------------------------
   AUTO REFRESH
-------------------------- */

setInterval(() => {

    predict();

}, 30000);


// USER REGISTRATION

async function registerUser() {

    const email =
        document.getElementById("email").value;

    const message =
        document.getElementById("message");

    message.innerText = "";

    if (!email.includes("@")) {

        message.innerText =
            "Please enter a valid email";

        return;
    }

    const res = await fetch("http://127.0.0.1:8000/register", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            email: email
        })
    });

    const data = await res.json();

    if (data.success) {

        message.style.color = "#22c55e";

        message.innerText =
            "Access Granted";

        setTimeout(() => {

            window.location.href =
                "/dashboard";

        }, 1200);
    }
}