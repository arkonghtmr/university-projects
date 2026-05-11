interface WireframeModalProps {
  title: string;
  onClose: () => void;
  isContactForm?: boolean;
}

export function WireframeModal({ title, onClose, isContactForm }: WireframeModalProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-[500px] p-8 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="w-64 h-8 bg-gray-400 rounded" />
          <button
            onClick={onClose}
            className="w-8 h-8 bg-gray-300 hover:bg-gray-400 rounded flex items-center justify-center"
          >
            ×
          </button>
        </div>

        {/* Form Fields */}
        <div className="space-y-4">
          {isContactForm ? (
            <>
              {/* Name */}
              <div className="space-y-2">
                <div className="w-16 h-4 bg-gray-300 rounded" />
                <div className="w-full h-10 bg-gray-100 border-2 border-gray-300 rounded" />
              </div>

              {/* Email */}
              <div className="space-y-2">
                <div className="w-16 h-4 bg-gray-300 rounded" />
                <div className="w-full h-10 bg-gray-100 border-2 border-gray-300 rounded" />
              </div>

              {/* Message */}
              <div className="space-y-2">
                <div className="w-24 h-4 bg-gray-300 rounded" />
                <div className="w-full h-32 bg-gray-100 border-2 border-gray-300 rounded" />
              </div>
            </>
          ) : (
            <>
              {/* Email/Login */}
              <div className="space-y-2">
                <div className="w-20 h-4 bg-gray-300 rounded" />
                <div className="w-full h-10 bg-gray-100 border-2 border-gray-300 rounded" />
              </div>

              {/* Password */}
              <div className="space-y-2">
                <div className="w-20 h-4 bg-gray-300 rounded" />
                <div className="w-full h-10 bg-gray-100 border-2 border-gray-300 rounded" />
              </div>

              {/* Remember Me / Forgot Password */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-gray-300 border border-gray-400 rounded" />
                  <div className="w-32 h-4 bg-gray-300 rounded" />
                </div>
                <div className="w-40 h-4 bg-gray-300 rounded" />
              </div>
            </>
          )}

          {/* Submit Button */}
          <button className="w-full h-12 bg-gray-600 hover:bg-gray-700 text-white rounded mt-4">
            {isContactForm ? 'Отправить' : 'Войти'}
          </button>

          {/* Additional Link */}
          {!isContactForm && (
            <div className="text-center">
              <div className="w-48 h-4 bg-gray-300 rounded mx-auto" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
