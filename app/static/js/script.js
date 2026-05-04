document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('summarizer-form');
    const sourceText = document.getElementById('source-text');
    const summaryText = document.getElementById('summary-text');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = sourceText.value.trim();
        if (!text) {
            summaryText.textContent = 'Please enter some text to summarize.';
            return;
        }

        summaryText.textContent = 'Generating summary...';

        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ dialogue: text })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || response.statusText);
            }

            const data = await response.json();
            summaryText.textContent = data.summary || 'No summary generated.';
        } catch (error) {
            console.error('Summarization error:', error);
            summaryText.textContent = `Failed to generate summary. ${error.message}`;
        }
    });
});
