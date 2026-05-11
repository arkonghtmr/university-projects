export function WireframeFeatures() {
  return (
    <section className="py-20 bg-white">
      <div className="w-[1300px] mx-auto px-4">
        {/* Section Title */}
        <div className="text-center mb-16 space-y-3">
          <div className="w-64 h-10 bg-gray-400 rounded mx-auto" />
          <div className="w-96 h-4 bg-gray-300 rounded mx-auto" />
        </div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-3 gap-8">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="bg-gray-50 border-2 border-gray-300 rounded-lg p-6 space-y-4"
            >
              {/* Icon */}
              <div className="w-16 h-16 bg-gray-400 rounded-lg" />

              {/* Title */}
              <div className="w-40 h-6 bg-gray-400 rounded" />

              {/* Description */}
              <div className="space-y-2">
                <div className="w-full h-3 bg-gray-300 rounded" />
                <div className="w-full h-3 bg-gray-300 rounded" />
                <div className="w-3/4 h-3 bg-gray-300 rounded" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
