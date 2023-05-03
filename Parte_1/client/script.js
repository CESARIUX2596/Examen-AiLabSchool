const data_url =
	"https://raw.githubusercontent.com/CESARIUX2596/Examen-AiLabSchool/master/Parte_1/data/test_final.csv";
const tbody = document.querySelector("#myTable tbody");

const labels = [];

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

// send data to local flask server for prediction and display the result in the label
document.getElementById("selected-data").addEventListener("submit", function (event) {
	event.preventDefault();

	const form = event.target;
	const data = {
		id: form.elements.id.value,
		gender: form.elements.gender.value,
		age: form.elements.age.value,
		hypertension: form.elements.hypertension.value,
		heart_disease: form.elements.heart_disease.value,
		ever_married: form.elements.ever_married.value,
		work_type: form.elements.work_type.value,
		Residence_type: form.elements.Residence_type.value,
		avg_glucose_level: form.elements.avg_glucose_level.value,
		bmi: form.elements.bmi.value,
		smoking_status: form.elements.smoking_status.value
	};
	
	// Send data to local flask server for prediction
	fetch("http://127.0.0.1:5000/predict", {
		method: "POST",
		body: JSON.stringify(data),
		headers: {
			"Content-Type": "application/json"
		}

	})
	.then((response) => response.json())
	.then(result => {
		// Display result as alert
		// Check if Stroke or No Stroke
		console.log(result.Prediction);
		// Cast prediction to int
		var prediction = parseInt(result.Prediction);
		if (prediction == 1) {
			// Add text to label Stroke
			document.getElementById("prediction-label").innerHTML = "Stroke";
			document.getElementById("prediction-label").style.color = "red";
		} else {
			document.getElementById("prediction-label").innerHTML = "No Stroke";
			document.getElementById("prediction-label").style.color = "green";
		}
	})
	.catch(error => {
		console.error('Error:', error);
	});
});