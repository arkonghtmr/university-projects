export function WireframeFooter() {
  return (
    <footer className="bg-gray-800 py-12">
      <div className="w-[1300px] mx-auto px-4">
        <div className="grid grid-cols-4 gap-8 mb-8">
          {/* Company Info */}
          <div className="space-y-4">
            <div className="w-32 h-8 bg-gray-400 rounded" />
            <div className="space-y-2">
              <div className="w-full h-3 bg-gray-500 rounded" />
              <div className="w-3/4 h-3 bg-gray-500 rounded" />
            </div>
          </div>

          {/* Links Column 1 */}
          <div className="space-y-3">
            <div className="w-24 h-5 bg-gray-400 rounded" />
            <div className="space-y-2">
              {Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="w-28 h-3 bg-gray-500 rounded" />
              ))}
            </div>
          </div>

          {/* Links Column 2 */}
          <div className="space-y-3">
            <div className="w-24 h-5 bg-gray-400 rounded" />
            <div className="space-y-2">
              {Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="w-32 h-3 bg-gray-500 rounded" />
              ))}
            </div>
          </div>

          {/* Contact */}
          <div className="space-y-3">
            <div className="w-28 h-5 bg-gray-400 rounded" />
            <div className="space-y-2">
              {Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="w-36 h-3 bg-gray-500 rounded" />
              ))}
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-gray-600 flex justify-between items-center">
          <div className="w-48 h-3 bg-gray-500 rounded" />
          <div className="flex gap-3">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="w-8 h-8 bg-gray-500 rounded-full" />
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
