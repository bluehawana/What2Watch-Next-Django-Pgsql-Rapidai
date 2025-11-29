export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-white">
          <h1 className="text-6xl font-bold mb-6">
            What2Watch
          </h1>
          <p className="text-2xl mb-8 text-gray-200">
            Your Personalized Content Discovery Platform
          </p>
          <p className="text-lg mb-12 text-gray-300 max-w-3xl mx-auto">
            Stop wasting time searching. Get personalized recommendations across all your
            streaming platforms, sports schedules, and TV programs - all in one place.
          </p>

          <div className="grid md:grid-cols-3 gap-8 mt-16 max-w-5xl mx-auto">
            <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
              <h3 className="text-xl font-semibold mb-4">Streaming Content</h3>
              <p className="text-gray-300">
                Discover movies and TV shows across Netflix, Disney+, Prime Video, and more
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
              <h3 className="text-xl font-semibold mb-4">Sports Schedules</h3>
              <p className="text-gray-300">
                Never miss your favorite team's match with personalized sports notifications
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
              <h3 className="text-xl font-semibold mb-4">Personalized Profiles</h3>
              <p className="text-gray-300">
                Customize your experience: Sports Fan, Movie Buff, Family, Kids, and more
              </p>
            </div>
          </div>

          <div className="mt-16">
            <p className="text-gray-400 text-sm">
              Coming soon to web, Android, and iOS
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
