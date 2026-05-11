interface WireframeCTAProps {
  onCTAClick: () => void;
}

export function WireframeCTA({ onCTAClick }: WireframeCTAProps) {
  return (
    <section className="py-20 bg-gray-600">
      <div className="w-[1300px] mx-auto px-4 text-center space-y-8">
        {/* Heading */}
        <div className="space-y-4">
          <div className="w-[600px] h-12 bg-gray-200 rounded mx-auto" />
          <div className="w-[500px] h-5 bg-gray-300 rounded mx-auto" />
        </div>

        {/* CTA Button */}
        <button
          onClick={onCTAClick}
          className="w-64 h-16 bg-white hover:bg-gray-100 border-2 border-gray-200 rounded mx-auto flex items-center justify-center"
        >
          <span className="text-gray-800">Связаться с нами</span>
        </button>
      </div>
    </section>
  );
}
