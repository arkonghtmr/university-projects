interface WireframeHeaderProps {
  onLoginClick: () => void;
}

export function WireframeHeader({ onLoginClick }: WireframeHeaderProps) {
  return (
    <header className="h-[120px] bg-gray-100 border-b-2 border-gray-400">
      <div className="w-[1300px] mx-auto h-full flex items-center justify-between px-4">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="w-12 h-12 bg-gray-400 rounded" />
          <div className="w-32 h-6 bg-gray-400 rounded" />
        </div>

        {/* Navigation */}
        <nav className="flex items-center gap-8">
          <div className="w-20 h-4 bg-gray-400 rounded" />
          <div className="w-24 h-4 bg-gray-400 rounded" />
          <div className="w-20 h-4 bg-gray-400 rounded" />
          <div className="w-28 h-4 bg-gray-400 rounded" />
          <div className="w-24 h-4 bg-gray-400 rounded" />
        </nav>

        {/* User Actions */}
        <div className="flex items-center gap-4">
          <div className="w-8 h-8 bg-gray-400 rounded-full" />
          <button
            onClick={onLoginClick}
            className="w-32 h-10 bg-gray-500 hover:bg-gray-600 rounded border-2 border-gray-600 flex items-center justify-center"
          >
            <span className="text-white text-sm">Войти</span>
          </button>
        </div>
      </div>
    </header>
  );
}
