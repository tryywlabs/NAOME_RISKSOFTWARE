export default function MetricCard({ label, value, delta, tone = 'neutral' }) {
  return (
    <article className={`metric-card metric-card--${tone}`}>
      <p className="metric-card__label">{label}</p>
      <p className="metric-card__value">{value}</p>
      <p className="metric-card__delta">{delta}</p>
    </article>
  );
}
