export default function ResultsDashboard() {
  const summary = {
    avgEmpathy: 0.84,
    safetyAccuracy: 0.96,
    crisisEscalationRate: 0.18,
    benchmarkSamples: 120,
  };

  const rows = [
    { dataset: 'EmpatheticDialogues', empathy: 0.88, safety: 0.95, strategy: 'emotional_validation' },
    { dataset: 'Custom Safety', empathy: 0.72, safety: 1.0, strategy: 'crisis_escalation' },
    { dataset: 'Academic Stress', empathy: 0.85, safety: 0.97, strategy: 'cognitive_reframing' },
  ];

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold">Agentic Therapy System — Evaluation Dashboard</h1>
          <p className="text-sm text-gray-600 mt-2">
            Research metrics for empathy, safety, and intervention planning.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <MetricCard title="Avg Empathy" value={summary.avgEmpathy} />
          <MetricCard title="Safety Accuracy" value={summary.safetyAccuracy} />
          <MetricCard title="Crisis Escalation" value={summary.crisisEscalationRate} />
          <MetricCard title="Samples" value={summary.benchmarkSamples} />
        </div>

        <div className="rounded-3xl shadow-sm border p-6">
          <h2 className="text-xl font-semibold mb-4">Benchmark Breakdown</h2>
          <table className="w-full text-left">
            <thead>
              <tr className="border-b">
                <th className="py-2">Dataset</th>
                <th className="py-2">Empathy</th>
                <th className="py-2">Safety</th>
                <th className="py-2">Top Strategy</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, idx) => (
                <tr key={idx} className="border-b last:border-0">
                  <td className="py-3">{row.dataset}</td>
                  <td>{row.empathy}</td>
                  <td>{row.safety}</td>
                  <td>{row.strategy}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value }) {
  return (
    <div className="rounded-3xl border shadow-sm p-5">
      <div className="text-sm text-gray-500">{title}</div>
      <div className="text-2xl font-bold mt-2">{value}</div>
    </div>
  );
}
