export default function LoadingState({ label = "Loading" }: { label?: string }) {
  return <p className="py-10 text-sm text-slate-500">{label}...</p>;
}
