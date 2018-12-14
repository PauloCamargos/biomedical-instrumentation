using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using uPLibrary.Networking.M2Mqtt.Utility;
using uPLibrary.Networking.M2Mqtt.Exceptions;

public class Player : MonoBehaviour
{
    Animator anim;
    string msg;
    MqttClient client;

    // Use this for initialization
    void Start()
    {
        anim = gameObject.GetComponentInChildren<Animator>();

        client = new MqttClient("127.0.0.1");
        client.MqttMsgPublishReceived += OnMqttMsgReceived;

        string clientId = Guid.NewGuid().ToString();
        client.Connect(clientId);

        client.Subscribe(new string[] {"move"},
        new byte[] {
            MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE }
        );

    }
    void OnMqttMsgReceived(object sender, MqttMsgPublishEventArgs e)
    {
        var topic = e.Topic;

        if (topic == "move")
        {
            msg = System.Text.Encoding.UTF8.GetString(e.Message);
        }
    }

    // Update is called once per frame
    void Update()
    {
        switch (msg)
        {
            case "fechar":
                anim.SetBool("play_fechar", true);
                Debug.Log("Fechando a mão...");
                break;
            case "abrir":
                anim.SetBool("play_fechar", false);
                Debug.Log("Abrindo a mão...");
                break;
            case "flexionar":
                anim.SetBool("play_flexao", true);
                Debug.Log("Realizando flexão da mão...");
                break;

            case "estender":
                anim.SetBool("play_flexao", false);
                Debug.Log("Realizando extensão da mão...");
                break;

            case "supinar":
                anim.SetTrigger("play_supinacao");
                Debug.Log("Realizando supinação da mão...");
                break;

            case "pronar":
                anim.SetTrigger("play_pronacao");
                Debug.Log("Realizando pronação da mão...");
                break;
        }


        if (Input.GetKey("down"))
        {
            anim.SetBool("play_fechar", true);
            Debug.Log("Fechando a mão...");
        }
        else if (Input.GetKey("up"))
        {
            anim.SetBool("play_fechar", false);
            Debug.Log("Abrindo a mão...");
        }
        else if (Input.GetKey("left"))
        {
            anim.SetBool("play_flexao", true);
            Debug.Log("Realizando flexão da mão...");

        }
        else if (Input.GetKey("right"))
        {
            anim.SetBool("play_flexao", false);
            Debug.Log("Realizando extensão da mão...");

        }
        else if (Input.GetKey("s"))
        {
            anim.SetTrigger("play_supinacao");
            Debug.Log("Realizando supinação da mão...");

        }
        else if (Input.GetKey("p"))
        {
            anim.SetTrigger("play_pronacao");
            Debug.Log("Realizando pronação da mão...");
        }
    }
}

