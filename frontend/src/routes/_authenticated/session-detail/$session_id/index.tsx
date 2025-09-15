import { createFileRoute } from '@tanstack/react-router'
import SessionDetail from '@/features/session-detail/$session_id'

export const Route = createFileRoute('/_authenticated/session-detail/$session_id/')({
  component: SessionDetail,
})
