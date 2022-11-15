package main

/*
#include <asm/types.h>
#include <sys/socket.h>
#include <linux/netlink.h>
#include <linux/inet_diag.h>
*/
import "C"

import (
	"fmt"
	"syscall"

	"github.com/sirupsen/logrus"
	"github.com/vishvananda/netlink/nl"
)

// type InetDiagReqV2 C.struct_inet_diag_req_v2
// type InetDiagMsg C.struct_inet_diag_msg

// const (
// 	SizeofInetDiagReqV2 = C.sizeof_struct_inet_diag_req_v2
// )

const TCPF_ALL = 0xFFF

//
// // linux/sock_diag.h
// const SOCK_DIAG_BY_FAMILY = 20
//
// const (
// 	_ = iota
// 	TCP_ESTABLISHED
// 	TCP_SYN_SENT
// 	TCP_SYN_RECV
// 	TCP_FIN_WAIT1
// 	TCP_FIN_WAIT2
// 	TCP_TIME_WAIT
// 	TCP_CLOSE
// 	TCP_CLOSE_WAIT
// 	TCP_LAST_ACK
// 	TCP_LISTEN
// 	TCP_CLOSING
// )
//
const (
	INET_DIAG_NONE = iota
	INET_DIAG_MEMINFO
	INET_DIAG_INFO
	INET_DIAG_VEGASINFO
	INET_DIAG_CONG
	INET_DIAG_TOS
	INET_DIAG_TCLASS
	INET_DIAG_SKMEMINFO
	INET_DIAG_SHUTDOWN
	INET_DIAG_DCTCPINFO
	INET_DIAG_PROTOCOL
	INET_DIAG_SKV6ONLY
)

//
// func showID(id C.struct_inet_diag_sockid) string {
// 	return fmt.Sprintf("%d", id.idiag_sport)
// }

func main() {
	req := nl.NewNetlinkRequest(SOCK_DIAG_BY_FAMILY, syscall.NLM_F_DUMP)
	{
		msg := NewInetDiagReqV2(syscall.AF_INET, syscall.IPPROTO_TCP, TCPF_ALL & ^((1<<TCP_SYN_RECV)|(1<<TCP_TIME_WAIT)|(1<<TCP_CLOSE)))
		// msg := InetDiagReqV2{
		// 	sdiag_family:   syscall.AF_INET,
		// 	sdiag_protocol: syscall.IPPROTO_TCP,
		// 	idiag_states:   TCPF_ALL & ^((1 << TCP_SYN_RECV) | (1 << TCP_TIME_WAIT) | (1 << TCP_CLOSE)),
		// }
		// msg.idiag_ext |= (1 << (INET_DIAG_INFO - 1))
		msg.IDiagExt |= (1 << (INET_DIAG_INFO - 1))
		req.AddData(msg)
	}

	res, err := req.Execute(syscall.NETLINK_INET_DIAG, 0)
	if err != nil {
		logrus.Error("req.Execute error: ", err)
		return
	}
	// fmt.Println("    Family State Timer Retrans  Expires  RQueue     WQueue     UID  INode")
	for _, data := range res {
		m := ParseInetDiagMsg(data)
		fmt.Println("[test] ", m)
		// m := (*InetDiagMsg)(unsafe.Pointer(&data[0]))
		// fmt.Println("\n\n", i, data)
		// fmt.Println(i, m)
		// fmt.Printf(
		// 	"%3d %-6d %-5d %-5d %-8d %-8d %-10d %-10d %-5d %-10d %s\n",
		// 	i,
		// 	m.idiag_family,
		// 	m.idiag_state,
		// 	m.idiag_timer,
		// 	m.idiag_retrans,
		// 	m.idiag_expires,
		// 	m.idiag_rqueue,
		// 	m.idiag_wqueue,
		// 	m.idiag_uid,
		// 	m.idiag_inode,
		// 	showID(m.id),
		// )
	}
}