export function GridOverlay() {
  return (
    <div className="fixed inset-0 pointer-events-none z-40">
      <div className="w-[1920px] h-full mx-auto">
        <div className="w-[1300px] h-full mx-auto grid grid-cols-12 gap-[20px]">
          {Array.from({ length: 12 }).map((_, i) => (
            <div
              key={i}
              className="bg-blue-500/10 border border-blue-500/30 h-full"
            />
          ))}
        </div>
      </div>
    </div>
  );
}
