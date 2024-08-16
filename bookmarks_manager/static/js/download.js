// author: opLynx
// date started: 2024-08-15 at 2025

const downloadFileContainer = document.querySelector('.download-file-container');
const hoverBox = document.getElementById('hover-box');
const progressBarContainer = document.getElementById('progress-bar-container');
const progressBar = document.getElementById('progress-bar');
const downloadComplete = document.getElementById('download-complete');

let downloadProgress = 0;
let downloadInterval;
let isHovering = false;
let isDragging = false;
let isHoldingOverBox = false;
let holdTimer;
const HOLD_TIME_BEFORE_STARTING_DOWNLOAD = 1; // instant
let originalPosition = {
    left: downloadFileContainer.offsetLeft,
    top: downloadFileContainer.offsetTop
};

// Pointer events to handle dragging
downloadFileContainer.style.position = 'absolute';

downloadFileContainer.addEventListener('pointerdown', (event) => {
    event.preventDefault();
    isDragging = true;
    hoverBox.style.opacity = '1';
    originalPosition = {
        left: downloadFileContainer.offsetLeft,
        top: downloadFileContainer.offsetTop
    };
    downloadFileContainer.setPointerCapture(event.pointerId); // Capture pointer to keep tracking
});

downloadFileContainer.addEventListener('pointermove', (event) => {
    if (isDragging) {
        downloadFileContainer.style.left = `${event.clientX}px`;
        downloadFileContainer.style.top = `${event.clientY}px`;

        // Check if the file container is over the hover box
        const rect = hoverBox.getBoundingClientRect();
        const containerRect = downloadFileContainer.getBoundingClientRect();

        if (containerRect.left >= rect.left && containerRect.right <= rect.right && containerRect.top >= rect.top && containerRect.bottom <= rect.bottom) {
            isHovering = true;
            if (!isHoldingOverBox) {
                holdTimer = setTimeout(() => {
                    startDownload();
                }, HOLD_TIME_BEFORE_STARTING_DOWNLOAD);
                isHoldingOverBox = true;
            }
        } else {
            isHovering = false;
            isHoldingOverBox = false;
            clearTimeout(holdTimer);
        }
    }
});

downloadFileContainer.addEventListener('pointerup', (event) => {
    if (isHoldingOverBox && isHovering) {
        clearTimeout(holdTimer);
        startDownload();
    }
    isDragging = false;
    resetProgress();
    resetFilePosition();
    hoverBox.style.opacity = '0.5';
    downloadFileContainer.releasePointerCapture(event.pointerId); // Release pointer capture
});

downloadFileContainer.addEventListener('pointercancel', () => {
    if (isDragging) {
        clearTimeout(holdTimer);
        resetProgress();
        resetFilePosition();
        downloadFileContainer.releasePointerCapture(event.pointerId); // Release pointer capture
    }
});
downloadFileContainer.addEventListener('pointerleave', () => {
    if (isDragging) {
        clearTimeout(holdTimer);
        resetProgress();
        resetFilePosition();
    }
});
function resetFilePosition() {
    // Ensure the container returns to the original position
    downloadFileContainer.style.left = originalPosition.left + 'px';
    downloadFileContainer.style.top = originalPosition.top + 'px';
}

// start the downloading progress and progress bar
function startDownload() {
    if (isHovering) {
        progressBarContainer.style.display = 'flex';
        downloadInterval = setInterval(() => {
            downloadProgress += 10;
            progressBar.style.width = `${downloadProgress}%`;

            if (downloadProgress >= 100) {
                clearInterval(downloadInterval);
                progressBar.style.width = '100%';
                downloadComplete.style.display = 'block';
                const fileUrl = downloadFileContainer.getAttribute('data-url');
                downloadFile(fileUrl);
            }

            if (!isHovering) {
                resetProgress();
            }
        }, 500);
    }
}

// resets progress bar
function resetProgress() {
    clearInterval(downloadInterval);
    progressBar.style.width = '0%';
    downloadProgress = 0;
    isHovering = false;
    progressBarContainer.style.display = 'none';
    downloadComplete.style.display = 'none';
}

// download file
function downloadFile(url) {
    const a = document.createElement('a');
    a.href = url;
    a.download = 'sample.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
