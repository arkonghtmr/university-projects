interface WireframeHeroProps {
  onCTAClick: () => void;
}

export function WireframeHero({ onCTAClick }: WireframeHeroProps) {
  return (
    <section className="h-[700px] bg-gray-50 border-b-2 border-gray-300">
      <div className="w-[1300px] mx-auto h-full flex items-center justify-between px-4">
        {/* Left Content */}
        <div className="flex-1 space-y-6">
          {/* Heading */}
          <div className="space-y-3">
            <div className="w-[500px] h-12 bg-gray-400 rounded" />
            <div className="w-[450px] h-12 bg-gray-400 rounded" />
          </div>

          {/* Description */}
          <div className="space-y-2">
            <div className="w-[480px] h-4 bg-gray-300 rounded" />
            <div className="w-[450px] h-4 bg-gray-300 rounded" />
            <div className="w-[420px] h-4 bg-gray-300 rounded" />
          </div>

          {/* CTA Buttons */}
          <div className="flex gap-4 pt-4">
            <button
              onClick={onCTAClick}
              className="w-48 h-14 bg-gray-600 hover:bg-gray-700 rounded border-2 border-gray-700 flex items-center justify-center"
            >
              <span className="text-white">Кнопка CTA</span>
            </button>
            <div className="w-48 h-14 bg-white border-2 border-gray-400 rounded flex items-center justify-center">
              <span className="text-gray-600">Вторая кнопка</span>
            </div>
          </div>
        </div>

        {/* Right Image Placeholder */}
        <div className="w-[550px] h-[500px] bg-gray-300 rounded-lg border-2 border-gray-400 flex items-center justify-center">
          <div className="text-gray-500 text-xl">Изображение / Иллюстрация</div>
        </div>
      </div>
    </section>
  );
}
