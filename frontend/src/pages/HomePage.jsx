import ChatWindow from '@/components/Chat/ChatWindow'
import FloatingControls from '@/components/Common/FloatingControls'

export default function HomePage() {
  return (
    <div className='h-full bg-background flex flex-col'>
        <div className='h-full'>
          <ChatWindow />
        </div>
        <FloatingControls />
    </div>
  )
}