"use strict";

function getType(typestr) {
    for (let type of ["bin", "dec", "hex"]) {
        if (typestr.includes(type)) {
            return type;
        }
    }
}

function getBaseValue(decint, type) {
    if (type === "bin") {
        return decint.toString(2);
    } else if (type === "dec") {
        return decint.toString();
    } else if (type === "hex") {
        return decint.toString(16).toUpperCase();
    } 
}

function getIntValue(numstr, type) {
    if (type === "bin") {
        return parseInt(numstr, 2);
    } else if (type === "dec") {
        return parseInt(numstr);
    } else if (type === "hex") {
        return parseInt(numstr, 16);
    } 
}

function getQn(tr) {
    for (let td of tr.querySelectorAll("td")) {
        if (td.classList.contains("qn")) {
            let type = getType(td.className);
            return {
                type: getType(td.className),
                value: getIntValue(td.innerHTML, type)
            };
        }
    }
}

function checkRow(tr, qn) {
    function isCorrect(td) {
        let type = getType(td.querySelector("input").name);
        let tdValue = getIntValue(td.querySelector("input").value, type);
        return tdValue === qn.value;
    }
    
    function checkAns(td) {
        td.querySelector("input").disabled = true;
        td.appendChild(document.createElement('br'));
        let feedback = document.createElement('p');
        if (isCorrect(td)) {
            feedback.classList.add("correct");
            feedback.innerHTML = '✔ Correct';
        } else {
            let type = getType(td.querySelector("input").name);
            feedback.classList.add("incorrect");
            feedback.innerHTML = `✘ Incorrect (${getBaseValue(qn.value, type)})`;
        }
        td.appendChild(feedback);
    }
    
    tr.querySelectorAll("td.ans").forEach(checkAns);
}

function checkQn(tr) {
    let qn = getQn(tr);
    checkRow(tr, qn);
}

function timeTaken() {
    let startTime = new Date(document.querySelector("#start-time").value.trimRight('Z') + '+0000');
    let duration = Math.floor((new Date() - startTime) / 1000);  // seconds
    let [min, sec] = [Math.floor(duration / 60), duration % 60]
    return `${min} min ${sec} sec`
}

function addDuration() {
    let th = document.createElement('th');
    th.classList.add("qn-col");
    th.innerHTML = 'Time Taken';
    let td = document.createElement('td');
    td.classList.add("ans-col");
    td.innerHTML = timeTaken();
    let tr = document.createElement('tr');
    tr.appendChild(th);
    tr.appendChild(td);
    document.querySelector("div#name-entry table").appendChild(tr);
}

function checkMyAns() {
    addDuration();
    document.querySelector("div#name-entry #student-name").disabled = true;    
    document.querySelectorAll("table.table tr.qn-row")
    .forEach(checkQn);

    let button = document.querySelector("button#check-my-ans");
    button.innerHTML = 'Try Again';
    button.onclick = () => window.location.reload();

    let help = document.createElement('p');
    help.innerHTML = '<a href="https://docs.google.com/spreadsheets/d/1X9LyBvEeUTKbi-ETXkBdmfxnvCdC8m2QuXX0AElI7LQ/edit?usp=share_link" target="_blank">How do I convert between binary, decimal, and hexadecimal?</a><br />(NYJC Google login required)'
    document.querySelector("div#submit-entry").insertBefore(help, button);
}

window.onload = () => document
    .querySelectorAll('input.ans')
    .forEach(input => {input.value = '';});