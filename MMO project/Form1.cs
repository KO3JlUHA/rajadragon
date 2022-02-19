using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MMO_project
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }


        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            pictureBox1.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\map.png");
            pictureBox1.Size = Size = new System.Drawing.Size(1600, 900);
            textBox1.Visible = false;
            textBox2.Visible = false; 
            button1.Visible = false;
            this.KeyPreview = true;
            pictureBox2.Visible = true;
        }

        private void Form1_KeyPress(object sender, KeyPressEventArgs e)
        {

        }

        private void textBox1_MouseClick(object sender, MouseEventArgs e)
        {
            if(textBox1.Text == "")
            {
                textBox1.Text = "username";
            }
        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.W && pictureBox1.Location.Y + pictureBox1.Height > 845)
            {
                pictureBox1.Location = new System.Drawing.Point(pictureBox1.Location.X, pictureBox1.Location.Y - 10);
                pictureBox2.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\upSprite.gif");
            }
            if (e.KeyCode == Keys.S && pictureBox1.Location.Y < 0)
            {
                pictureBox1.Location = new System.Drawing.Point(pictureBox1.Location.X, pictureBox1.Location.Y + 10);
                pictureBox2.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\downSprite.gif");
            }
            if (e.KeyCode == Keys.D && pictureBox1.Location.X < 0)
            {
                pictureBox1.Location = new System.Drawing.Point(pictureBox1.Location.X + 10, pictureBox1.Location.Y);
                pictureBox2.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\rightSprite.gif");
            }
            if (e.KeyCode == Keys.A && pictureBox1.Location.X + pictureBox1.Width > 1540)
            {
                pictureBox1.Location = new System.Drawing.Point(pictureBox1.Location.X - 10, pictureBox1.Location.Y);
                pictureBox2.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\leftSprite.gif");
            }
        }

        private void Form1_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.W)
            {
                pictureBox2.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\up1.jpg");

            }
            if (e.KeyCode == Keys.S)
            {
                pictureBox2.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\down1.jpg");

            }
            if (e.KeyCode == Keys.D)
            {
                pictureBox2.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\right1.jpg");

            }
            if (e.KeyCode == Keys.A)
            {
                pictureBox2.Image = Image.FromFile(@"C:\Networks\work\mmo project 2 window forms\MMO project\left1.jpg");
            }
        }
    }

}
