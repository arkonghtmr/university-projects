export function WireframeProducts() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="w-[1300px] mx-auto px-4">
        {/* Section Title */}
        <div className="text-center mb-16 space-y-3">
          <div className="w-80 h-10 bg-gray-400 rounded mx-auto" />
          <div className="w-[500px] h-4 bg-gray-300 rounded mx-auto" />
        </div>

        {/* Product Cards Grid */}
        <div className="grid grid-cols-4 gap-6">
          {Array.from({ length: 8 }).map((_, i) => (
            <div
              key={i}
              className="bg-white border-2 border-gray-300 rounded-lg overflow-hidden"
            >
              {/* Product Image */}
              <div className="w-full h-48 bg-gray-300 flex items-center justify-center">
                <div className="text-gray-500">Фото</div>
              </div>

              {/* Product Info */}
              <div className="p-4 space-y-3">
                <div className="w-full h-5 bg-gray-400 rounded" />
                <div className="w-3/4 h-3 bg-gray-300 rounded" />
                <div className="w-full h-3 bg-gray-300 rounded" />

                {/* Price and Button */}
                <div className="flex items-center justify-between pt-2">
                  <div className="w-20 h-6 bg-gray-400 rounded" />
                  <div className="w-24 h-8 bg-gray-600 rounded" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
