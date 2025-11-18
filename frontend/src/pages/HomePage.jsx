import ChatWindow from '@/components/Chat/ChatWindow'
import FloatingControls from '@/components/Common/FloatingControls'
import MobileHeader from '@/components/Common/MobileHeader'

export default function HomePage({ onMenuClick, currentThreadId }) {
  return (
    <div className='h-full bg-background flex flex-col'>
      {/* Mobile Header - only show on mobile */}
      {onMenuClick && (
        <div className='md:hidden'>
          <MobileHeader onMenuClick={onMenuClick} />
        </div>
      )}

      <div className='flex-1 flex flex-col overflow-hidden'>
        <ChatWindow currentThreadId={currentThreadId} />
      </div>

      {/* Floating controls - responsive positioning */}
      <FloatingControls />
    </div>
  )
}