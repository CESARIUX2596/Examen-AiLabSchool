const data_url =
	"https://raw.githubusercontent.com/CESARIUX2596/Examen-AiLabSchool/master/Parte_1/data/test.csv";
const tbody = document.querySelector("#myTable tbody");

const labels_url = 
	"https://raw.githubusercontent.com/CESARIUX2596/Examen-AiLabSchool/master/Parte_1/data/test_target.csv";

const labels = [];

// Fetch the labels
fetch(labels_url)
	.then((response) => response.text())
	.then((data) => {
		const rows = data.split("\n");

		for (let i = 1; i < 31; i++) {
			const cells = rows[i].split(",");
			labels.push(cells[0]);
		}
	})
	.catch((error) => console.error(error));


// Fetch the CSV file and populate the table
fetch(data_url)
	.then((response) => response.text())
	.then((data) => {
		const rows = data.split("\n");

		for (let i = 1; i < 31; i++) {
			const cells = rows[i].split(",");
			const row = document.createElement("tr");
			// Read the expected predictions from the test_targets.csv file

			// Add event listener to the row
			row.addEventListener("click", function () {
				const data = {
					id: cells[0],
					gender: cells[1],
					age: cells[2],
					hypertension: cells[3],
					heart_disease: cells[4],
					ever_married: cells[5],
					work_type: cells[6],
					Residence_type: cells[7],
					avg_glucose_level: cells[8],
					bmi: cells[9],
					smoking_status: cells[10],
					Expected_Prediction: cells[11]
				};

				// Send data to fields in the prediction-container input fields
				document.querySelector("#id").value = data.id;
				document.querySelector("#age").value = data.age;
				document.querySelector("#gender").value = data.gender;
				document.querySelector("#hypertension").value = data.hypertension;
				document.querySelector("#heart_disease").value = data.heart_disease;
				document.querySelector("#ever_married").value = data.ever_married;
				document.querySelector("#work_type").value = data.work_type;
				document.querySelector("#Residence_type").value = data.Residence_type;
				document.querySelector("#avg_glucose_level").value = data.avg_glucose_level;
				document.querySelector("#bmi").value = data.bmi;
				document.querySelector("#smoking_status").value = data.smoking_status;
			});

			for (let j = 0; j < cells.length; j++) {
				const cell = document.createElement("td");
				cell.textContent = cells[j];
				row.appendChild(cell);
			}

			tbody.appendChild(row);
		}
	})
	.catch((error) => console.error(error));

// Send data to the server from the form
const form = document.querySelector("#prediction-container");
form.addEventListener("submit", (e) => {
	e.preventDefault();

	const formData = new FormData(form);
	const data = Object.fromEntries(formData);

	// Send data to the server
	fetch("/predict", {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(data)
	})
	.then((response) => response.json())

	// Display the prediction
	.then((data) => {
		const prediction = document.querySelector("#prediction");
		prediction.textContent = data.prediction;
	})
	.catch((error) => console.error(error));
});

	