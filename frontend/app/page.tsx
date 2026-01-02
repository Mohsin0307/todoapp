import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm flex flex-col gap-8">
        <h1 className="text-4xl font-bold text-center">
          Hackathon Todo
        </h1>

        <p className="text-center text-lg max-w-2xl">
          Multi-user task management application with JWT authentication.
          Organize your tasks, track progress, and boost productivity.
        </p>

        <div className="flex gap-4 items-center justify-center flex-wrap">
          <Link
            href="/login"
            className="rounded-lg bg-primary-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-primary-700 focus:outline-none focus:ring focus:ring-primary-300"
          >
            Log In
          </Link>

          <Link
            href="/signup"
            className="rounded-lg border border-primary-600 px-5 py-3 text-sm font-medium text-primary-600 transition hover:bg-primary-50 focus:outline-none focus:ring focus:ring-primary-300"
          >
            Sign Up
          </Link>
        </div>

        <div className="mt-8 grid text-center lg:grid-cols-3 lg:text-left gap-4 max-w-4xl">
          <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
            <h2 className="mb-3 text-2xl font-semibold">
              Fast & Secure{' '}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                →
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-50">
              JWT authentication with httpOnly cookies for maximum security.
            </p>
          </div>

          <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
            <h2 className="mb-3 text-2xl font-semibold">
              User-Scoped{' '}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                →
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-50">
              Each user has their own private task list with full CRUD operations.
            </p>
          </div>

          <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
            <h2 className="mb-3 text-2xl font-semibold">
              Modern Stack{' '}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                →
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-50">
              Built with Next.js 15, React 19, FastAPI, and PostgreSQL.
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
