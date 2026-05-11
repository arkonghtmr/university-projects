export function WireframeTestimonials() {
  return (
    <section className="py-20 bg-white">
      <div className="w-[1300px] mx-auto px-4">
        {/* Section Title */}
        <div className="text-center mb-16 space-y-3">
          <div className="w-72 h-10 bg-gray-400 rounded mx-auto" />
          <div className="w-[450px] h-4 bg-gray-300 rounded mx-auto" />
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-3 gap-8">
          {Array.from({ length: 3 }).map((_, i) => (
            <div
              key={i}
              className="bg-gray-50 border-2 border-gray-300 rounded-lg p-6 space-y-4"
            >
              {/* Stars */}
              <div className="flex gap-1">
                {Array.from({ length: 5 }).map((_, j) => (
                  <div key={j} className="w-5 h-5 bg-gray-400 rounded" />
                ))}
              </div>

              {/* Quote */}
              <div className="space-y-2">
                <div className="w-full h-3 bg-gray-300 rounded" />
                <div className="w-full h-3 bg-gray-300 rounded" />
                <div className="w-full h-3 bg-gray-300 rounded" />
                <div className="w-4/5 h-3 bg-gray-300 rounded" />
              </div>

              {/* Author */}
              <div className="flex items-center gap-3 pt-2">
                <div className="w-12 h-12 bg-gray-400 rounded-full" />
                <div className="space-y-2">
                  <div className="w-32 h-4 bg-gray-400 rounded" />
                  <div className="w-24 h-3 bg-gray-300 rounded" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
