const showHideBtn = document.getElementById('toggleButton');
const modal = document.getElementById('modal');

updateButtonText();

showHideBtn.addEventListener('click', function() {
    modal.classList.toggle('hidden');
    updateButtonText();
});

function updateButtonText() {
    const isModalHidden = modal.classList.contains('hidden');
    showHideBtn.innerHTML = isModalHidden ? "Add" : "Close";
}


function saveSleep() {
    // Get values from form
    let bedtimeString = document.getElementById("bedtime").value;
    let riseString = document.getElementById("rise").value;
    let date = document.getElementById("date").value;

    // Check if bedtime and rise are in the valid format (HH:mm)
    if (!/^\d{2}:\d{2}$/.test(bedtimeString) || !/^\d{2}:\d{2}$/.test(riseString)) {
        alert("Invalid time format. Please use HH:mm format.");
        return;
    }

    // Convert HH:mm strings to Date objects
    let bedtime = new Date('1970-01-01T' + bedtimeString);
    let rise = new Date('1970-01-01T' + riseString);

    // Check if Date objects are valid
    if (isNaN(bedtime.getTime()) || isNaN(rise.getTime())) {
        alert("Invalid time values. Please enter valid times.");
        return;
    }

    // Calculate hours and minutes of sleep
    let timeDifference = rise - bedtime;
    let hours = Math.floor(timeDifference / (60 * 60 * 1000));
    let minutes = Math.floor((timeDifference % (60 * 60 * 1000)) / (60 * 1000));

    // Get existing sleep data from localStorage or initialize an empty array
    let sleepData = JSON.parse(localStorage.getItem("sleepData")) || [];

    // Add new sleep entry
    let newEntry = { bedtime: bedtime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), rise: rise.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), date: date, hoursOfSleep: `${hours} hours ${minutes} minutes` };
    sleepData.push(newEntry);

    // Save updated sleep data to localStorage
    localStorage.setItem("sleepData", JSON.stringify(sleepData));

    clearForm();

    modal.classList.toggle('hidden');
    updateButtonText();
    // Display all stored data on the page
    displaySleepData();

    // Optionally, display a confirmation message
    // alert("Sleep data saved!");
}



// 
// 
function formatDate(dateString) {
    const date = new Date(dateString);
    const day = date.getDate();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };

    let daySuffix = 'th';
    if (day >= 11 && day <= 13) {
        daySuffix = 'th';
    } else {
        switch (day % 10) {
            case 1:
                daySuffix = 'st';
                break;
            case 2:
                daySuffix = 'nd';
                break;
            case 3:
                daySuffix = 'rd';
                break;
        }
    }

    const formattedDate = new Intl.DateTimeFormat(undefined, options).format(date);
    return formattedDate.replace(/\d{1,2}/, match => match + daySuffix);
}


function displaySleepData() {
        let sleepData = JSON.parse(localStorage.getItem("sleepData")) || [];
        let sleepList = document.getElementById("sleepList");
        sleepList.innerHTML = "";

        sleepData.reverse().forEach(function (entry) {
            let listItem = document.createElement("li");
            listItem.innerHTML = `
            <div class="mb-2 bg-white p-1 pb-0 rounded">

                <div class="bg-red-100 px-2 flex justify-between items-center">
                  <p class="text-gray-700"><span class="font-bold">Sleep</span></p>
                  <p class="bg-green-400 -mr-2 p-1 text-white text-right"><span class="">${entry.hoursOfSleep}</span></p>
                </div>
                
                <div class="bg-green-50 px-2 flex justify-between items-center">
                  <p class="text-gray-700"><span class="font-bold">Bedtime</span></p>
                  <p class="text-gray-700">${entry.bedtime}</p>
                </div>
                
                <div class="bg-yellow-50 px-2 flex justify-between items-center">
                  <p class="text-gray-700"><span class="font-bold">Rise</span></p>
                  <p class="text-gray-700">${entry.rise}</p>
                </div>
                
                <div class="bg-blue-50 px-2 flex justify-between items-center">
                  <p class="text-gray-700"><span class="font-bold">Date</span></p>
                  <p class="text-gray-700">${formatDate(entry.date)}</p>
                </div>
              
            <!-- \container -->
            </div>
        `;
        sleepList.appendChild(listItem);
        });
    }


// 
// 
function clearForm() {
    // Reset form values
    document.getElementById("bedtime").value = "";
    document.getElementById("rise").value = "";
    document.getElementById("date").value = "";
}


function clearLocalStorage() {
    // Clear all local storage data
    localStorage.removeItem("sleepData");

    // Clear the displayed sleep data
    displaySleepData();
}

// Display existing data on page load
displaySleepData();


// 
// 

function downloadData() {
    const sleepData = localStorage.getItem("sleepData");

    if (sleepData) {
        const blob = new Blob([sleepData], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'sleep_data.txt';
        document.body.appendChild(a);
        a.click();

        // Cleanup
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } else {
        alert("No sleep data available to download.");
    }
}