import { useRouter } from '@tanstack/react-router'

export default function Dashboard() {
  const router = useRouter()
  router.navigate({ to: '/benchmarks'})
}