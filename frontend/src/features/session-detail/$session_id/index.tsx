import { useCallback, useEffect, useState } from 'react'
import { useRouter } from '@tanstack/react-router'
import {
  copySession,
  getDependencies,
  getllmDetail,
  getllms,
  getSessionDetail,
  getSessionDetailTurnhistory,
  playTurn,
  updateSession,
} from '@/apis/turnbench'
import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import { CheckIcon, ChevronsUpDownIcon } from 'lucide-react'
import { toast } from 'sonner'
import { cn } from '@/lib/utils'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
  DialogClose,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { Switch } from '@/components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'

export default function Setups() {
  const router = useRouter()
  const [session_data, setSessionData] = useState<any>({})
  const [onShowHiddenMapping, setOnShowHiddenMapping] = useState(false)
  const [onShowHiddenCritria, setOnShowHiddenCritria] = useState(false)
  const [onShowComparison, setOnShowComparison] = useState(false)
  const [showHoverCard, setShowHoverCard] = useState(false)
  const [curChangeData, setCurChangeData] = useState<any>({})
  const [onShowLeftDT, setOnShowLeftDT] = useState(false)
  const [onShowRightDT, setOnShowRightDT] = useState(false)
  const [onSelectSession, setOnSelectSession] = useState({
    left: 0,
    right: 0,
  })

  const [currentEditText, setCurrentEditText] = useState<any>()

  const [leftNodes, setLeftNodes] = useState<any>([])
  const [leftEdges, setLeftEdges] = useState<any>([])

  const [rightNodes, setRightNodes] = useState<any>([])
  const [rightEdges, setRightEdges] = useState<any>([])
  const onNodesChange = useCallback(
    (changes: any) =>
      setLeftNodes((nodesSnapshot: any) =>
        applyNodeChanges(changes, nodesSnapshot)
      ),
    []
  )
  const onEdgesChange = useCallback(
    (changes: any) =>
      setLeftEdges((edgesSnapshot: any) =>
        applyEdgeChanges(changes, edgesSnapshot)
      ),
    []
  )
  const onConnect = useCallback(
    (params: any) =>
      setLeftEdges((edgesSnapshot: any) => addEdge(params, edgesSnapshot)),
    []
  )

  const [models, setModels] = useState<{ id: string; display_name: string }[]>(
    []
  )
  const [openModel, setOpenModel] = useState(false)
  const [selectModel, setSelectModel] = useState({
    id: '',
    display_name: '',
  })

  const [localSessionData, setLocalSessionData] = useState<any>([])
  useEffect(() => {
    // 获取当前路由路径
    const path = router.state.location.pathname
    // to do  get sessionid
    const session_id = path.split('/')[2]
    getSessionDetail(session_id).then((res: any) => {
      setSessionData(res.data.data)
      const llm_id = res.data.data.llm_id

      getllmDetail(llm_id).then((llmres: any) => {
        getSessionDetailTurnhistory(session_id).then((hisres: any) => {
          const sessionHistory = hisres.data.data
          sessionHistory.forEach((element: any) => {
            element['showAll'] = false
            element['canEdit'] = false
          })
          let data = {
            session_id: res.data.data.id,
            llm_id: llm_id,
            model_name: llmres.data.data.display_name,
            model_nick_name: llmres.data.data.display_name,
            isLoading: false,
            data: sessionHistory,
          }
          let curSessionData = [data]
          setLocalSessionData(curSessionData)
        })
      })
    })
    getllms({ page: 1, page_size: 100 }).then((res: any) => {
      setModels(res.data.data || [])
    })
  }, [router.state.location.pathname])

  const showHiddenMapping = (game_info: any, index: number) => {
    const nightmare_verifier_ids = game_info.nightmare_verifier_ids
    const verifier_id = game_info.verifier_ids[index]
    return nightmare_verifier_ids.findIndex((item: any) => item === verifier_id)
  }

  const onShowLeftContinueBtn = () => {
    const index = onSelectSession.left
    return localSessionData[index].data.findIndex((item: any) => item.is_game_over) === -1
  }

  const onShowRightContinueBtn = () => {
    const index = onSelectSession.right
    return localSessionData[index].data.findIndex((item: any) => item.is_game_over) === -1
  }

  return (
    <div className='flex flex-1 flex-col p-8'>
      {/* 顶部区域：两侧四个Label和一个按钮 */}
      <div className='mb-8 flex items-center justify-between'>
        {/* 左侧两个Label */}
        <div className='flex'>
          <div className='mr-4 flex'>
            <Label className='mr-1'>ID:</Label>{' '}
            <div>{session_data?.game_info?.id}</div>
          </div>
          <div className='mr-4 flex'>
            <Label className='mr-1'>Difficulty:</Label>{' '}
            {session_data?.game_info?.difficulty}
          </div>
          <div className='mr-4 flex'>
            <Label className='mr-1'>Mode:</Label> {session_data?.mode}
          </div>
          <div className='mr-4 flex'>
            <Label className='mr-1'>Answer:</Label>{' '}
            {session_data?.game_info?.answer}
          </div>
        </div>
        {/* 右侧两个Label和一个按钮 */}
        <div className='flex flex-col items-end space-y-4'>
          <Button
            onClick={() => {
              router.navigate({
                to: '/dataset',
              })
            }}
          >
            Exit Game
          </Button>
        </div>
      </div>
      {/* 下方四块区域 */}
      <div className='flex flex-1 flex-col'>
        <div className='flex'>
          <div className='flex h-16 w-116 rounded border p-4'>
            <div className='flex flex-row'>
              {session_data?.mode === 'nightmare' && (
                <div className='mr-4 flex items-center'>
                  <Switch
                    className='mr-2'
                    checked={onShowHiddenMapping}
                    onCheckedChange={setOnShowHiddenMapping}
                  />
                  <Label>Show Hidden Mapping</Label>
                </div>
              )}
              <div className='flex items-center'>
                <Switch
                  className='mr-2'
                  checked={onShowHiddenCritria}
                  onCheckedChange={setOnShowHiddenCritria}
                />
                <Label>Show Hidden Active Critria</Label>
              </div>
            </div>
          </div>
          <div className='ml-4 flex h-16 flex-1 items-center justify-between rounded border p-4'>
            <div>Thinking Process</div>
            <div className='flex items-center'>
              <Switch
                className='mr-2'
                checked={onShowComparison}
                onCheckedChange={setOnShowComparison}
              />
              <Label>Comparison Mode</Label>
            </div>
          </div>
        </div>

        <div className='mt-4 flex flex-1'>
          <div className='flex w-116 flex-col rounded border p-4'>
            {session_data?.game_info?.verifier_details.map(
              (verifer: any, index: number) => (
                <div
                  className='mt-2 shadow-sm'
                  style={{ padding: '4px 8px', borderRadius: '8px' }}
                >
                  <div className='flex justify-between'>
                    <Badge className='verifer-title'>Verifer {index}</Badge>
                    {onShowHiddenMapping && (
                      <Badge className='verifer-title-hidden'>
                        Verifer{' '}
                        {showHiddenMapping(session_data.game_info, index)}
                      </Badge>
                    )}
                  </div>

                  <div>{verifer.description}</div>
                  <div className='verifer-content'>
                    {verifer.criteria.map((criteria: any, c_index: number) => (
                      <li
                        style={{
                          fontWeight:
                            c_index ===
                              session_data?.game_info?.active_criteria_ids[
                                index
                              ] && onShowHiddenCritria
                              ? '600'
                              : '400',
                          backgroundColor:
                            c_index ===
                              session_data?.game_info?.active_criteria_ids[
                                index
                              ] && onShowHiddenCritria
                              ? 'color-mix(in oklab, oklch(57.7% .245 27.325) 10%, transparent)'
                              : '#fff',
                        }}
                      >
                        {criteria.description}
                      </li>
                    ))}
                  </div>
                </div>
              )
            )}
          </div>


          <div className='ml-4 flex flex-1 justify-between rounded border p-4'>
            <Tabs
              defaultValue={localSessionData?.[0]?.model_name}
              className='relative'
              style={{
                width: onShowComparison ? '48%' : '99%',
                height: 'calc(100vh - 300px)',
                overflowY: 'auto',
              }}
            >
              <div className='flex items-center justify-between'>
                <TabsList>
                  {localSessionData.map((session: any, index: number) => (
                    <TabsTrigger
                      value={session?.model_name}
                      onClick={() => {
                        const selectSession = { ...onSelectSession }
                        selectSession.left = index
                        setOnSelectSession(selectSession)
                      }}
                    >
                      {session?.model_name}
                    </TabsTrigger>
                  ))}
                </TabsList>
                <div className='flex items-center'>
                  <Switch
                    className='mr-2'
                    checked={onShowLeftDT}
                    onCheckedChange={() => {
                      setOnShowLeftDT(!onShowLeftDT)
                      if (!onShowLeftDT) {
                        const session_id =
                          localSessionData[onSelectSession.left].session_id
                        getSessionDetailTurnhistory(session_id).then(
                          (hisres: any) => {
                            const sessionHistory = hisres.data.data.map(
                              (item: any) => {
                                const itemNew = {
                                  turn_num: item.turn_num,
                                  reasoning: item.turn_reasoning,
                                }
                                return itemNew
                              }
                            )
                            getDependencies({
                              llm_id:
                                localSessionData[onSelectSession.left].llm_id,
                              reasoning_history: sessionHistory,
                            }).then((res: any) => {
                              const nodes: {
                                id: any
                                position: { x: number; y: number }
                                data: { label: string }
                              }[] = []
                              const edges: {
                                id: string
                                source: any
                                target: any
                              }[] = []
                              res.data.data.forEach(
                                (element: any, index: number) => {
                                  const historyItem = hisres.data.data.find(
                                    (item: any) =>
                                      item.turn_num === element.current_turn
                                  )
                                  const node = {
                                    id: element.current_turn.toString(),
                                    position: { x: 0, y: index * 100 },
                                    data: {
                                      label: `Turn ${element.current_turn} Round ${historyItem.round_num}\n`,
                                    },
                                  }
                                  nodes.push(node)

                                  if (element.dependency_turns) {
                                    element.dependency_turns.forEach(
                                      (dep: any) => {
                                        const edge = {
                                          id: `e${dep}_to_${element.current_turn}`,
                                          source: dep.toString(),
                                          target:
                                            element.current_turn.toString(),
                                          animated: true,
                                        }
                                        edges.push(edge)
                                      }
                                    )
                                  }
                                }
                              )
                              setLeftNodes(nodes)
                              setLeftEdges(edges)
                            })
                          }
                        )
                      }
                    }}
                  />
                  <Label>Show DT</Label>
                </div>
              </div>

              {localSessionData.map((session: any, index: number) => (
                <>
                  <TabsContent
                    value={session?.model_name}
                    className='w-full overflow-auto flex-none'
                    style={{ height: 'calc(100% - 90px)' }}
                  >
                    {onShowLeftDT && (
                      <>
                        <div style={{ width: '100%', height: '100%' }}>
                          <ReactFlow
                            nodes={leftNodes}
                            edges={leftEdges}
                            onNodesChange={onNodesChange}
                            onEdgesChange={onEdgesChange}
                            onConnect={onConnect}
                            fitView
                          >
                            <Controls />
                            <MiniMap />
                            <Background gap={12} size={1} />
                          </ReactFlow>
                        </div>
                      </>
                    )}
                    {!onShowLeftDT && (
                      <>
                        {session.data.map(
                          (sessionItem: any, itemIndex: number) => (
                            <div className='mt-[8px] w-full border shadow-sm'>
                              <div className='flex items-center justify-between'>
                                <div className='items-center text-black'>
                                  Turn {sessionItem.turn_num} Round{' '}
                                  {sessionItem.round_num} -{' '}
                                  {sessionItem.turn_name}
                                </div>
                                <div className='flex items-center'>
                                  <Dialog>
                                    <form>
                                      <DialogTrigger asChild>
                                        <Button
                                          className='ml-[8px]'
                                          variant='outline'
                                          onClick={() => {
                                            const currentData =
                                              sessionItem.turn_prompt
                                            setCurrentEditText(currentData)
                                          }}
                                        >
                                          Step Prompt
                                        </Button>
                                      </DialogTrigger>
                                      <DialogContent className='sm:max-w-[600px]'>
                                        <DialogHeader>
                                          <DialogTitle>Prompt</DialogTitle>
                                          <DialogDescription>
                                            <Textarea
                                              className='sm:max-h-[400px]'
                                              defaultValue={
                                                sessionItem.turn_prompt
                                              }
                                              onChange={(e) => {
                                                setCurrentEditText(
                                                  e.target.value
                                                )
                                              }}
                                            />
                                          </DialogDescription>
                                        </DialogHeader>
                                        <DialogFooter>
                                          <DialogClose>
                                            <Button
                                              type='submit'
                                              onClick={() => {
                                                //更新session
                                              }}
                                            >
                                              Save
                                            </Button>
                                          </DialogClose>
                                          <DialogClose asChild>
                                            <Button>Cancel</Button>
                                          </DialogClose>
                                        </DialogFooter>
                                      </DialogContent>
                                    </form>
                                  </Dialog>

                                  <Button
                                    className='ml-4'
                                    variant='outline'
                                    onClick={() => {
                                      const sessionData_cur =
                                        localSessionData.map((model: any) => {
                                          return { ...model }
                                        })
                                      sessionData_cur[index].data[
                                        itemIndex
                                      ].showAll =
                                        !sessionData_cur[index].data[itemIndex]
                                          .showAll
                                      setLocalSessionData(sessionData_cur)
                                    }}
                                  >
                                    Expand
                                  </Button>
                                </div>
                              </div>

                              {sessionItem.showAll && (
                                <div className='p-[5px]'>
                                  <div className='flex items-center justify-between'>
                                    <div>Reasoning:</div>
                                    {!sessionItem.canEdit && (
                                      <div>
                                        {sessionItem.turn_name === 'Deduce' && (
                                          <Button variant='outline'>
                                            Evaluation
                                          </Button>
                                        )}

                                        <Button
                                          className='ml-[8px]'
                                          variant='outline'
                                          onClick={() => {
                                            const sessionData_cur =
                                              localSessionData.map(
                                                (model: any) => {
                                                  return { ...model }
                                                }
                                              )
                                            sessionData_cur[index].data[
                                              itemIndex
                                            ].canEdit = true
                                            setLocalSessionData(sessionData_cur)
                                            setCurrentEditText(
                                              sessionData_cur[index]
                                            )
                                          }}
                                        >
                                          Edit
                                        </Button>
                                      </div>
                                    )}

                                    {sessionItem.canEdit && (
                                      <div>
                                        <Button
                                          variant='outline'
                                          onClick={() => {
                                            setShowHoverCard(!showHoverCard)
                                            const sessionItemData = {
                                              sessionItem: {
                                                ...sessionItem,
                                                canEdit: false,
                                              },
                                              session_id: session.session_id,
                                            }
                                            setCurChangeData(sessionItemData)
                                          }}
                                        >
                                          Save
                                        </Button>
                                        <Button
                                          variant='outline'
                                          className='ml-[8px]'
                                          onClick={() => {
                                            const sessionData_cur =
                                              localSessionData.map(
                                                (model: any) => {
                                                  return { ...model }
                                                }
                                              )
                                            getSessionDetail(
                                              sessionData_cur[index].session_id
                                            ).then((res: any) => {
                                              sessionData_cur[index].data[
                                                itemIndex
                                              ].turn_reasoning =
                                                res.data.data.turn_result_history[
                                                  itemIndex
                                                ].turn_reasoning
                                              sessionData_cur[index].data[
                                                itemIndex
                                              ].canEdit = false
                                              sessionData_cur[index].data[
                                                itemIndex
                                              ].showAll = false
                                              setLocalSessionData(
                                                sessionData_cur
                                              )
                                            })
                                          }}
                                        >
                                          Cancel
                                        </Button>
                                      </div>
                                    )}
                                  </div>
                                  <div className='content-mid'>
                                    <Textarea
                                      defaultValue={sessionItem.turn_reasoning}
                                      disabled={!sessionItem.canEdit}
                                      onChange={(e) => {
                                        const currentData = {
                                          ...currentEditText,
                                        }
                                        currentData.data[
                                          itemIndex
                                        ].turn_reasoning = e.target.value
                                        setCurrentEditText(currentData)
                                      }}
                                    />
                                  </div>
                                  <div className='content-bottom'>
                                    {sessionItem.turn_name === 'proposal' && (
                                      <div className='flex items-center'>
                                        <div className='mr-[8px] whitespace-nowrap'>
                                          Decision:
                                        </div>
                                        <Input
                                          disabled={!sessionItem.canEdit}
                                          value={sessionItem.guess_code}
                                          type='text'
                                        />
                                      </div>
                                    )}

                                    {sessionItem.turn_name === 'question' && (
                                      <div className='flex items-center'>
                                        <div className='mr-[8px] whitespace-nowrap'>
                                          Decision:
                                        </div>
                                        <Input
                                          disabled={!sessionItem.canEdit}
                                          value={sessionItem.verifier_choice}
                                          type='text'
                                        />
                                        <div className='mr-[8px] ml-[24px] whitespace-nowrap'>
                                          Feedback:
                                        </div>
                                        <Input
                                          disabled={!sessionItem.canEdit}
                                          value={sessionItem.verifier_result}
                                          type='text'
                                        />
                                      </div>
                                    )}

                                    {sessionItem.turn_name === 'deduce' && (
                                      <div className='flex items-center'>
                                        <div className='mr-[8px] whitespace-nowrap'>
                                          Decision:
                                        </div>
                                        {sessionItem.deduce_choice_skip && (
                                          <Input
                                            disabled
                                            value='continue'
                                            type='text'
                                          />
                                        )}
                                        {!sessionItem.deduce_choice_skip && (
                                          <Input
                                            disabled
                                            value='Submit'
                                            type='text'
                                          />
                                        )}

                                        {!sessionItem.deduce_choice_skip && (
                                          <div className='mr-[8px] ml-[24px] whitespace-nowrap'>
                                            Verifier Code:
                                          </div>
                                        )}

                                        {!sessionItem.deduce_choice_skip && (
                                          <Input
                                            disabled
                                            value={
                                              sessionItem.deduce_choice_submit_code
                                            }
                                            type='text'
                                          />
                                        )}

                                        {!sessionItem.deduce_choice_skip && (
                                          <div className='mr-[8px] ml-[24px] whitespace-nowrap'>
                                            Feedback:
                                          </div>
                                        )}

                                        {!sessionItem.deduce_choice_skip && (
                                          <Input
                                            disabled
                                            value={
                                              sessionItem.game_success
                                                ? 'WIN'
                                                : 'FAIL'
                                            }
                                            type='text'
                                          />
                                        )}
                                      </div>
                                    )}
                                  </div>
                                </div>
                              )}
                            </div>
                          )
                        )}
                      </>
                    )}
                  </TabsContent>
                  
                  <div className='absolute right-0 bottom-0 flex w-full justify-end bg-white'>
                    {onShowLeftContinueBtn() && !localSessionData[onSelectSession.left]?.isLoading && (
                      <Button
                        variant='outline'
                        onClick={() => {
                          const index = onSelectSession.left
                          const sessionData_cur = localSessionData.map(
                            (model: any) => {
                              return { ...model }
                            }
                          )
                          sessionData_cur[index].isLoading = true
                          setLocalSessionData(sessionData_cur)
                          playTurn(localSessionData[index].session_id, {}).then((res: any) => {
                            const nextPromptData = {
                              ...res.data.data,
                            }
                            nextPromptData['showAll'] = true
                            nextPromptData['canEdit'] = false
                            const sessionData_new = [...sessionData_cur]
                            sessionData_new[index].data.push(nextPromptData)
                            sessionData_new[index].isLoading = false
                            setLocalSessionData(sessionData_new)
                          })
                        }}
                      >
                        Continue
                      </Button>
                    )}
                    {onShowLeftContinueBtn() && localSessionData[onSelectSession.left].isLoading && (
                      <Button disabled variant='outline'>
                        Loading
                      </Button>
                    )}
                  </div>
                </>
              ))}
            </Tabs>

            {onShowComparison && (
              <Tabs
              defaultValue={localSessionData?.[0]?.model_name}
              className='relative'
              style={{
                width: onShowComparison ? '48%' : '99%',
                height: 'calc(100vh - 300px)',
                overflowY: 'auto',
              }}
            >
              <div className='flex items-center justify-between'>
                <TabsList>
                  {localSessionData.map((session: any, index: number) => (
                    <TabsTrigger
                      value={session?.model_name}
                      onClick={() => {
                        const selectSession = { ...onSelectSession }
                        selectSession.right = index
                        setOnSelectSession(selectSession)
                      }}
                    >
                      {session?.model_name}
                    </TabsTrigger>
                  ))}
                </TabsList>
                <div className='flex items-center'>
                  <Switch
                    className='mr-2'
                    checked={onShowRightDT}
                    onCheckedChange={() => {
                      setOnShowRightDT(!onShowRightDT)
                      if (!onShowRightDT) {
                        const session_id =
                          localSessionData[onSelectSession.right].session_id
                        getSessionDetailTurnhistory(session_id).then(
                          (hisres: any) => {
                            const sessionHistory = hisres.data.data.map(
                              (item: any) => {
                                const itemNew = {
                                  turn_num: item.turn_num,
                                  reasoning: item.turn_reasoning,
                                }
                                return itemNew
                              }
                            )
                            console.log('77777', localSessionData)
                            console.log('77777', onSelectSession)
                            getDependencies({
                              llm_id:
                                localSessionData[onSelectSession.right].llm_id,
                              reasoning_history: sessionHistory,
                            }).then((res: any) => {
                              const nodes: {
                                id: any
                                position: { x: number; y: number }
                                data: { label: string }
                              }[] = []
                              const edges: {
                                id: string
                                source: any
                                target: any
                              }[] = []
                              res.data.data.forEach(
                                (element: any, index: number) => {
                                  const historyItem = hisres.data.data.find(
                                    (item: any) =>
                                      item.turn_num === element.current_turn
                                  )
                                  const node = {
                                    id: element.current_turn.toString(),
                                    position: { x: 0, y: index * 100 },
                                    data: {
                                      label: `Turn ${element.current_turn} Round ${historyItem.round_num}\n`,
                                    },
                                  }
                                  nodes.push(node)

                                  if (element.dependency_turns) {
                                    element.dependency_turns.forEach(
                                      (dep: any) => {
                                        const edge = {
                                          id: `e${dep}_to_${element.current_turn}`,
                                          source: dep.toString(),
                                          target:
                                            element.current_turn.toString(),
                                          animated: true,
                                        }
                                        edges.push(edge)
                                      }
                                    )
                                  }
                                }
                              )
                              setRightNodes(nodes)
                              setRightEdges(edges)
                            })
                          }
                        )
                      }
                    }}
                  />
                  <Label>Show DT</Label>
                </div>
              </div>

              {localSessionData.map((session: any, index: number) => (
                <>
                  <TabsContent
                    value={session?.model_name}
                    className='w-full overflow-auto flex-none'
                    style={{ height: 'calc(100% - 90px)' }}
                  >
                    {onShowRightDT && (
                      <>
                        <div style={{ width: '100%', height: '100%' }}>
                          <ReactFlow
                            nodes={rightNodes}
                            edges={rightEdges}
                            onNodesChange={onNodesChange}
                            onEdgesChange={onEdgesChange}
                            onConnect={onConnect}
                            fitView
                          >
                            <Controls />
                            <MiniMap />
                            <Background gap={12} size={1} />
                          </ReactFlow>
                        </div>
                      </>
                    )}
                    {!onShowRightDT && (
                      <>
                        {session.data.map(
                          (sessionItem: any, itemIndex: number) => (
                            <div className='mt-[8px] w-full border shadow-sm'>
                              <div className='flex items-center justify-between'>
                                <div className='items-center text-black'>
                                  Turn {sessionItem.turn_num} Round{' '}
                                  {sessionItem.round_num} -{' '}
                                  {sessionItem.turn_name}
                                </div>
                                <div className='flex items-center'>
                                  <Dialog>
                                    <form>
                                      <DialogTrigger asChild>
                                        <Button
                                          className='ml-[8px]'
                                          variant='outline'
                                          onClick={() => {
                                            const currentData =
                                              sessionItem.turn_prompt
                                            setCurrentEditText(currentData)
                                          }}
                                        >
                                          Step Prompt
                                        </Button>
                                      </DialogTrigger>
                                      <DialogContent className='sm:max-w-[600px]'>
                                        <DialogHeader>
                                          <DialogTitle>Prompt</DialogTitle>
                                          <DialogDescription>
                                            <Textarea
                                              className='sm:max-h-[400px]'
                                              defaultValue={
                                                sessionItem.turn_prompt
                                              }
                                              onChange={(e) => {
                                                setCurrentEditText(
                                                  e.target.value
                                                )
                                              }}
                                            />
                                          </DialogDescription>
                                        </DialogHeader>
                                        <DialogFooter>
                                          <DialogClose>
                                            <Button
                                              type='submit'
                                              onClick={() => {
                                                //更新session
                                              }}
                                            >
                                              Save
                                            </Button>
                                          </DialogClose>
                                          <DialogClose asChild>
                                            <Button>Cancel</Button>
                                          </DialogClose>
                                        </DialogFooter>
                                      </DialogContent>
                                    </form>
                                  </Dialog>

                                  <Button
                                    className='ml-4'
                                    variant='outline'
                                    onClick={() => {
                                      const sessionData_cur =
                                        localSessionData.map((model: any) => {
                                          return { ...model }
                                        })
                                      sessionData_cur[index].data[
                                        itemIndex
                                      ].showAll =
                                        !sessionData_cur[index].data[itemIndex]
                                          .showAll
                                      setLocalSessionData(sessionData_cur)
                                    }}
                                  >
                                    Expand
                                  </Button>
                                </div>
                              </div>

                              {sessionItem.showAll && (
                                <div className='p-[5px]'>
                                  <div className='flex items-center justify-between'>
                                    <div>Reasoning:</div>
                                    {!sessionItem.canEdit && (
                                      <div>
                                        {sessionItem.turn_name === 'Deduce' && (
                                          <Button variant='outline'>
                                            Evaluation
                                          </Button>
                                        )}

                                        <Button
                                          className='ml-[8px]'
                                          variant='outline'
                                          onClick={() => {
                                            const sessionData_cur =
                                              localSessionData.map(
                                                (model: any) => {
                                                  return { ...model }
                                                }
                                              )
                                            sessionData_cur[index].data[
                                              itemIndex
                                            ].canEdit = true
                                            setLocalSessionData(sessionData_cur)
                                            setCurrentEditText(
                                              sessionData_cur[index]
                                            )
                                          }}
                                        >
                                          Edit
                                        </Button>
                                      </div>
                                    )}

                                    {sessionItem.canEdit && (
                                      <div>
                                        <Button
                                          variant='outline'
                                          onClick={() => {
                                            setShowHoverCard(!showHoverCard)
                                            const sessionItemData = {
                                              sessionItem: {
                                                ...sessionItem,
                                                canEdit: false,
                                              },
                                              session_id: session.session_id,
                                            }
                                            setCurChangeData(sessionItemData)
                                          }}
                                        >
                                          Save
                                        </Button>
                                        <Button
                                          variant='outline'
                                          className='ml-[8px]'
                                          onClick={() => {
                                            const sessionData_cur =
                                              localSessionData.map(
                                                (model: any) => {
                                                  return { ...model }
                                                }
                                              )
                                            getSessionDetail(
                                              sessionData_cur[index].session_id
                                            ).then((res: any) => {
                                              sessionData_cur[index].data[
                                                itemIndex
                                              ].turn_reasoning =
                                                res.data.data.turn_result_history[
                                                  itemIndex
                                                ].turn_reasoning
                                              sessionData_cur[index].data[
                                                itemIndex
                                              ].canEdit = false
                                              sessionData_cur[index].data[
                                                itemIndex
                                              ].showAll = false
                                              setLocalSessionData(
                                                sessionData_cur
                                              )
                                            })
                                          }}
                                        >
                                          Cancel
                                        </Button>
                                      </div>
                                    )}
                                  </div>
                                  <div className='content-mid'>
                                    <Textarea
                                      defaultValue={sessionItem.turn_reasoning}
                                      disabled={!sessionItem.canEdit}
                                      onChange={(e) => {
                                        const currentData = {
                                          ...currentEditText,
                                        }
                                        currentData.data[
                                          itemIndex
                                        ].turn_reasoning = e.target.value
                                        setCurrentEditText(currentData)
                                      }}
                                    />
                                  </div>
                                  <div className='content-bottom'>
                                    {sessionItem.turn_name === 'proposal' && (
                                      <div className='flex items-center'>
                                        <div className='mr-[8px] whitespace-nowrap'>
                                          Decision:
                                        </div>
                                        <Input
                                          disabled={!sessionItem.canEdit}
                                          value={sessionItem.guess_code}
                                          type='text'
                                        />
                                      </div>
                                    )}

                                    {sessionItem.turn_name === 'question' && (
                                      <div className='flex items-center'>
                                        <div className='mr-[8px] whitespace-nowrap'>
                                          Decision:
                                        </div>
                                        <Input
                                          disabled={!sessionItem.canEdit}
                                          value={sessionItem.verifier_choice}
                                          type='text'
                                        />
                                        <div className='mr-[8px] ml-[24px] whitespace-nowrap'>
                                          Feedback:
                                        </div>
                                        <Input
                                          disabled={!sessionItem.canEdit}
                                          value={sessionItem.verifier_result}
                                          type='text'
                                        />
                                      </div>
                                    )}

                                    {sessionItem.turn_name === 'deduce' && (
                                      <div className='flex items-center'>
                                        <div className='mr-[8px] whitespace-nowrap'>
                                          Decision:
                                        </div>
                                        {sessionItem.deduce_choice_skip && (
                                          <Input
                                            disabled
                                            value='continue'
                                            type='text'
                                          />
                                        )}
                                        {!sessionItem.deduce_choice_skip && (
                                          <Input
                                            disabled
                                            value='Submit'
                                            type='text'
                                          />
                                        )}

                                        {!sessionItem.deduce_choice_skip && (
                                          <div className='mr-[8px] ml-[24px] whitespace-nowrap'>
                                            Verifier Code:
                                          </div>
                                        )}

                                        {!sessionItem.deduce_choice_skip && (
                                          <Input
                                            disabled
                                            value={
                                              sessionItem.deduce_choice_submit_code
                                            }
                                            type='text'
                                          />
                                        )}

                                        {!sessionItem.deduce_choice_skip && (
                                          <div className='mr-[8px] ml-[24px] whitespace-nowrap'>
                                            Feedback:
                                          </div>
                                        )}

                                        {!sessionItem.deduce_choice_skip && (
                                          <Input
                                            disabled
                                            value={
                                              sessionItem.game_success
                                                ? 'WIN'
                                                : 'FAIL'
                                            }
                                            type='text'
                                          />
                                        )}
                                      </div>
                                    )}
                                  </div>
                                </div>
                              )}
                            </div>
                          )
                        )}
                      </>
                    )}
                  </TabsContent>
                  <div className='absolute right-0 bottom-0 flex w-full justify-end bg-white'>
                    {onShowRightContinueBtn() && !localSessionData[onSelectSession.right]?.isLoading && (
                      <Button
                        variant='outline'
                        onClick={() => {
                          const index = localSessionData.findIndex(
                            (item: any) =>
                              item.session_id === session.session_id
                          )
                          const sessionData_cur = localSessionData.map(
                            (model: any) => {
                              return { ...model }
                            }
                          )
                          sessionData_cur[index].isLoading = true
                          setLocalSessionData(sessionData_cur)
                          playTurn(session.session_id, {}).then((res: any) => {
                            const nextPromptData = {
                              ...res.data.data,
                            }
                            nextPromptData['showAll'] = true
                            nextPromptData['canEdit'] = false
                            const sessionData_new = [...sessionData_cur]
                            sessionData_new[index].data.push(nextPromptData)
                            sessionData_new[index].isLoading = false
                            setLocalSessionData(sessionData_new)
                          })
                        }}
                      >
                        Continue
                      </Button>
                    )}
                    {onShowRightContinueBtn() && localSessionData[onSelectSession.right]?.isLoading && (
                      <Button disabled variant='outline'>
                        Loading
                      </Button>
                    )}
                  </div>
                </>
              ))}
            </Tabs>
            )}
          </div>
        </div>
      </div>

      {showHoverCard && (
        <div
          className='absolute top-[-100px] left-[-32px] z-2 flex h-screen w-screen items-center justify-center'
          style={{ backgroundColor: 'rgba(0, 0, 0, 0.6)' }}
        >
          <div className='h-[220px] w-[800px] rounded-[8px] bg-white px-[48px] py-[72px]'>
            <div className=''>
              Please confirm whether you want to modify the current game session
              or create a new one.
            </div>
            <div className='mt-[4px] text-sm text-gray-500'>
              Creating a new session allows you to choose a different model. The
              new session will inherit the history of the current session,
              enabling comparison of strategy changes across models.
            </div>
            <div className='mt-[24px] flex justify-between'>
              <Button
                variant='outline'
                onClick={() => {
                  const sessionData = [...localSessionData]
                  sessionData.map((res: any) => {
                    if (res.session_id === curChangeData.session_id) {
                      res.data.map((item: any) => {
                        if (
                          item.turn_num ===
                            curChangeData.sessionItem.turn_num &&
                          item.round_num === curChangeData.sessionItem.round_num
                        ) {
                          item['turn_reasoning'] =
                            curChangeData.sessionItem.turn_reasoning
                          item['turn_prompt'] =
                            curChangeData.sessionItem.turn_prompt
                          item['canEdit'] = false
                        }
                      })
                    }
                  })
                  setLocalSessionData(sessionData)
                  updateSession(
                    curChangeData.session_id,
                    curChangeData.sessionItem
                  ).then((res: any) => {
                    toast('', {
                      description: 'Edit Success',
                    })
                    setShowHoverCard(!showHoverCard)
                  })
                }}
              >
                Save to Current Session
              </Button>

              <Dialog>
                <DialogTrigger as-child>
                  <Button variant='outline'>Create New Session</Button>
                </DialogTrigger>
                <DialogContent className='sm:max-w-[425px]'>
                  <DialogHeader>
                    <DialogDescription>
                      <div className='flex'>
                        <Label className='mr-4'>Model:</Label>
                        <Popover open={openModel} onOpenChange={setOpenModel}>
                          <PopoverTrigger asChild>
                            <Button
                              variant='outline'
                              role='combobox'
                              aria-expanded={openModel}
                              className='w-[200px] justify-between'
                            >
                              {selectModel.display_name
                                ? selectModel.display_name
                                : 'Select model...'}
                              <ChevronsUpDownIcon className='ml-2 h-4 w-4 shrink-0 opacity-50' />
                            </Button>
                          </PopoverTrigger>
                          <PopoverContent className='w-[200px] p-0'>
                            <Command>
                              <CommandInput placeholder='Search model...' />
                              <CommandList>
                                <CommandEmpty>No model found.</CommandEmpty>
                                <CommandGroup>
                                  {models.map((model) => (
                                    <CommandItem
                                      key={model.display_name}
                                      value={model.display_name}
                                      onSelect={(currentValue) => {
                                        setSelectModel(model)
                                        setOpenModel(false)
                                      }}
                                    >
                                      <CheckIcon
                                        className={cn(
                                          'mr-2 h-4 w-4',
                                          selectModel.display_name ===
                                            model.display_name
                                            ? 'opacity-100'
                                            : 'opacity-0'
                                        )}
                                      />
                                      {model.display_name}
                                    </CommandItem>
                                  ))}
                                </CommandGroup>
                              </CommandList>
                            </Command>
                          </PopoverContent>
                        </Popover>
                      </div>
                    </DialogDescription>
                  </DialogHeader>
                  <DialogFooter>
                    <DialogClose>
                      <Button
                        type='submit'
                        onClick={() => {
                          copySession(
                            curChangeData.session_id,
                            selectModel.id,
                            curChangeData.sessionItem
                          ).then((res: any) => {
                            const newSessionId = res.data.data
                            getSessionDetail(curChangeData.session_id).then(
                              (res: any) => {
                                const sessionData = res.data.data
                                const originData = [...localSessionData]
                                originData[0].data.map(
                                  (item: any, index: any) => {
                                    item['turn_prompt'] =
                                      sessionData.turn_result_history[
                                        index
                                      ].turn_prompt
                                    item['turn_reasoning'] =
                                      sessionData.turn_result_history[
                                        index
                                      ].turn_reasoning
                                    item['canEdit'] = false
                                    item['showAll'] = false
                                  }
                                )
                                let nameSet = new Set()
                                originData.map((item: any) => {
                                  nameSet.add(item.model_nickname)
                                })
                                const llm_id = selectModel.id
                                getllmDetail(llm_id).then((llmres: any) => {
                                  const originName =
                                    llmres.data.data.display_name
                                  let index = 1
                                  while (
                                    nameSet.has(originName + 'copy' + index)
                                  ) {
                                    index++
                                  }
                                  const newName = nameSet.has(originName)
                                    ? originName + 'copy' + index
                                    : originName
                                  const localSessionDataNew = [...originData]

                                  getSessionDetailTurnhistory(
                                    newSessionId
                                  ).then((res: any) => {
                                    const sessionTurnData = res.data.data
                                    sessionTurnData.map((item: any) => {
                                      item['showAll'] = false
                                      item['canEdit'] = false
                                    })
                                    const localSessionDataNewObj = {
                                      session_id: newSessionId,
                                      model_name: newName,
                                      model_nick_name: newName,
                                      llm_id: llm_id,
                                      isLoading: false,
                                      data: sessionTurnData,
                                    }

                                    localSessionDataNew.push(
                                      localSessionDataNewObj
                                    )
                                    setLocalSessionData(localSessionDataNew)
                                    setShowHoverCard(!showHoverCard)
                                  })
                                })
                              }
                            )
                          })
                        }}
                      >
                        Save
                      </Button>
                    </DialogClose>
                    <DialogClose>
                      <Button type='submit'>Cancel</Button>
                    </DialogClose>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
