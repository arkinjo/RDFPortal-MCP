// Browser Console Timer for Claude.ai Validation
// Copy and paste this into your browser's developer console (F12 → Console)

(function() {
    // Timer state
    window.validationTimer = {
        startTime: null,
        results: [],
        questionNum: 0,
        
        start: function() {
            this.questionNum++;
            this.startTime = performance.now();
            console.log(`⏱️ Timer STARTED for Q${this.questionNum.toString().padStart(3, '0')}`);
            console.log(`   Time: ${new Date().toLocaleTimeString()}`);
        },
        
        end: function(notes = '') {
            if (!this.startTime) {
                console.log('❌ No timer running! Use validationTimer.start() first');
                return;
            }
            const elapsed = (performance.now() - this.startTime) / 1000;
            const result = {
                question: `Q${this.questionNum.toString().padStart(3, '0')}`,
                time_sec: Math.round(elapsed * 100) / 100,
                notes: notes
            };
            this.results.push(result);
            console.log(`⏹️ Timer STOPPED: ${result.time_sec}s`);
            this.startTime = null;
        },
        
        list: function() {
            console.table(this.results);
            if (this.results.length > 0) {
                const total = this.results.reduce((sum, r) => sum + r.time_sec, 0);
                const avg = total / this.results.length;
                console.log(`Total: ${total.toFixed(1)}s | Avg: ${avg.toFixed(1)}s`);
            }
        },
        
        export: function() {
            // Export as CSV
            const csv = ['question,time_sec,notes']
                .concat(this.results.map(r => `${r.question},${r.time_sec},"${r.notes}"`))
                .join('\n');
            console.log('CSV Output:');
            console.log(csv);
            
            // Also copy to clipboard
            navigator.clipboard.writeText(csv).then(() => {
                console.log('✅ Copied to clipboard!');
            });
        },
        
        reset: function() {
            this.questionNum = 0;
            this.results = [];
            this.startTime = null;
            console.log('Timer reset');
        }
    };
    
    // Shortcuts
    window.ts = () => validationTimer.start();
    window.te = (n) => validationTimer.end(n);
    window.tl = () => validationTimer.list();
    window.tx = () => validationTimer.export();
    
    console.log(`
╔═══════════════════════════════════════════════════════╗
║         Validation Timer Loaded!                      ║
╠═══════════════════════════════════════════════════════╣
║  Quick Commands:                                      ║
║    ts()     - Start timer                             ║
║    te()     - End timer                               ║
║    te('note') - End timer with note                   ║
║    tl()     - List all results                        ║
║    tx()     - Export as CSV (copies to clipboard)     ║
║                                                       ║
║  Full Commands:                                       ║
║    validationTimer.start()                            ║
║    validationTimer.end()                              ║
║    validationTimer.list()                             ║
║    validationTimer.export()                           ║
║    validationTimer.reset()                            ║
╚═══════════════════════════════════════════════════════╝
    `);
})();
