package collectors

type Pod struct {
	Name            string
	Uid             string
	NodeName        string
	RequestMilliCpu int64
	RequestMemory   int64
}

type Resource struct {
	MilliCpu float64
	Memory   float64
}

type Storage_value struct {
	Total_size float64
	Size float64
}

type Latency_value struct {
	Min float64
	Max float64
	Avg float64
}

type Node struct {
	Name string
	Resource
}

type Storage struct {
	Name string
	Storage_value
}

type Network struct {
	Name string
	Latency_value
}

type User struct {
	Uid      string
	Priority float64
	index    int
}

type PriorityQueue []*User

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the lowest Priority, so we use smaller than here.
	return pq[i].Priority < pq[j].Priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	user := x.(*User)
	user.index = n
	*pq = append(*pq, user)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	user := old[n-1]
	user.index = -1 // for safety
	*pq = old[0 : n-1]
	return user
}
