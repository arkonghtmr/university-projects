import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

export function Program() {
  const [openModule, setOpenModule] = useState<number | null>(0);

  const modules = [
    {
      week: 'Неделя 1-2',
      title: 'Основы анимации и After Effects',
      lessons: [
        'Введение в моушн-дизайн: история, примеры, сферы применения',
        'Интерфейс After Effects: панели, композиции, слои',
        '12 принципов анимации Диснея',
        'Ключевые кадры и работа с таймлайном',
        'Анимация формы и трансформации',
        'Проект: создание простой анимированной инфографики',
      ],
    },
    {
      week: 'Неделя 3-4',
      title: 'Продвинутые техники в After Effects',
      lessons: [
        'Работа с масками и матами',
        'Эффекты и пресеты: правильное применение',
        'Анимация текста: preset animator и вручную',
        'Родительские связи (parenting) и null-объекты',
        'Выражения (expressions) для автоматизации',
        'Проект: анимированный типографический постер',
      ],
    },
    {
      week: 'Неделя 5-6',
      title: 'Основы 3D-анимации в Cinema 4D',
      lessons: [
        'Интерфейс Cinema 4D: навигация, примитивы, деформеры',
        'Моделирование простых объектов',
        'Материалы и текстуры: настройка и применение',
        'Освещение трёхточечной схемой',
        'Камеры и композиция кадра',
        'Проект: анимация 3D-логотипа',
      ],
    },
    {
      week: 'Неделя 7-8',
      title: 'Финальные проекты и шоурил',
      lessons: [
        'Создание сложной сцены с персонажем',
        'Работа со звуком и синхронизация с анимацией',
        'Цветокоррекция и финальный рендер',
        'Экспорт для разных платформ (Instagram, YouTube, Behance)',
        'Сборка шоурила из всех проектов',
        'Защита финального проекта перед наставником',
      ],
    },
  ];

  return (
    <section id="program" className="py-20 relative">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Программа курса</h2>
          <p className="text-xl text-gray-400">
            8 недель интенсивного обучения с практическими заданиями
          </p>
        </div>

        <div className="space-y-4 max-w-4xl mx-auto">
          {modules.map((module, index) => (
            <div
              key={index}
              className="bg-white/5 border border-white/10 rounded-xl overflow-hidden hover:border-purple-500/50 transition-colors"
            >
              <button
                onClick={() => setOpenModule(openModule === index ? null : index)}
                className="w-full p-6 flex items-center justify-between text-left hover:bg-white/5 transition-colors"
              >
                <div className="flex-1">
                  <div className="text-sm text-purple-400 mb-1">{module.week}</div>
                  <div className="text-xl font-bold">{module.title}</div>
                </div>
                <ChevronDown
                  size={24}
                  className={`text-gray-400 transition-transform ${
                    openModule === index ? 'rotate-180' : ''
                  }`}
                />
              </button>

              {openModule === index && (
                <div className="px-6 pb-6 border-t border-white/10">
                  <ul className="space-y-3 mt-4">
                    {module.lessons.map((lesson, lessonIndex) => (
                      <li
                        key={lessonIndex}
                        className="flex items-start gap-3 text-gray-300"
                      >
                        <span className="flex-shrink-0 w-6 h-6 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-xs font-bold mt-0.5">
                          {lessonIndex + 1}
                        </span>
                        <span>{lesson}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
