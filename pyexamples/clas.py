import sys

sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # input
    # to_input('../examples/clas/1.avi'),

    # block-downsample
    to_ConvConvRelu(name='conv0', s_filer=256, n_filer=(32, 32), offset="(0,0,0)", to="(0,0,0)",
                    width=(2, 2), height=40, depth=40),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(conv0-east)", width=1, height=36, depth=36, opacity=0.5),
    *block_2ConvPool(name='conv1', botton='pool_b1', top='pool_b2', s_filer=128, n_filer=64, offset="(2,0,0)",
                     size=(32, 32, 3), opacity=0.5),
    *block_2ConvPool(name='conv2', botton='pool_b2', top='pool_b3', s_filer=64, n_filer=128, offset="(2,0,0)",
                     size=(28, 28, 4), opacity=0.5),
    *block_2ConvPool(name='conv3', botton='pool_b3', top='pool_b4', s_filer=32, n_filer=256, offset="(2,0,0)",
                     size=(24, 24, 7), opacity=0.5),
    *block_2ConvPool(name='conv4', botton='pool_b4', top='pool_b5', s_filer=16, n_filer=256, offset="(2,0,0)",
                     size=(20, 20, 7), opacity=0.5),
    # *block_2ConvPool( name='conv5', botton='pool_b4', top='pool_b5', s_filer=8, n_filer=256, offset="(2,0,0)", size=(20,20,7), opacity=0.5 ),

    # Bottleneck
    # block-002
    to_ConvConvRelu(name='conv5', s_filer=8, n_filer=(256, 256), offset="(2,0,0)", to="(pool_b5-east)", width=(7, 7),
                    height=16, depth=16),
    to_connection("pool_b5", "conv5"),

    # Decoder
    to_UnPool(name='up1', offset="(2,0,0)", to="(conv5-east)", width=1, height=20, depth=20, opacity=0.5, caption=" "),
    to_connection("conv5", "up1"),
    to_Concate(name='conv6', s_filer=16, n_filer=256+256, offset="(0,0,0)", to="(up1-east)", width=14, height=20, depth=20, caption="concatenate 256+256"),
    to_skip(of='ccr_conv4', to='conv6', pos=1.25),
    to_ConvConvRelu(name='conv6_2', s_filer=16, n_filer=(128,128), offset="(0,0,0)", to="(conv6-east)", width=(4,4), height=20, depth=20, caption=" "),

    to_UnPool(name='up2', offset="(2,0,0)", to="(conv6_2-east)", width=1, height=24, depth=24, opacity=0.5, caption=" "),
    to_connection("conv6_2", "up2"),
    to_Concate(name='conv7', s_filer=32, n_filer=256+128, offset="(0,0,0)", to="(up2-east)", width=11, height=24, depth=24, caption="concatenate 256+128"),
    to_skip(of='ccr_conv3', to='conv7', pos=1.25),
    to_ConvConvRelu(name='conv7_2', s_filer=32, n_filer=(64,64), offset="(0,0,0)", to="(conv7-east)", width=(7,7), height=24, depth=24, caption=" "),

    to_UnPool(name='up3', offset="(2,0,0)", to="(conv7_2-east)", width=1, height=28, depth=28, opacity=0.5, caption=" "),
    to_connection("conv7_2", "up3"),
    to_Concate(name='conv8', s_filer=64, n_filer=128+64, offset="(0,0,0)", to="(up3-east)", width=7, height=28, depth=28, caption="concatenate 128+64"),
    to_skip(of='ccr_conv2', to='conv8', pos=1.25),
    to_ConvConvRelu(name='conv8_2', s_filer=64, n_filer=(32,32), offset="(0,0,0)", to="(conv8-east)", width=(4,4), height=28, depth=28, caption=" "),


    to_UnPool(name='up4', offset="(2,0,0)", to="(conv8_2-east)", width=1, height=32, depth=32, opacity=0.5, caption=" "),
    to_connection("conv8_2", "up4"),
    to_Concate(name='conv9', s_filer=128, n_filer=64+32, offset="(0,0,0)", to="(up4-east)", width=5, height=32, depth=32, caption="concatenate 64+32"),
    to_skip(of='ccr_conv1', to='conv9', pos=1.25),
    to_ConvConvRelu(name='conv9_2', s_filer=128, n_filer=(32,32), offset="(0,0,0)", to="(conv9-east)", width=(3,3), height=32, depth=32, caption=" "),

    to_UnPool(name='up5', offset="(2,0,0)", to="(conv9_2-east)", width=1, height=40, depth=40, opacity=0.5, caption=" "),
    to_connection("conv9_2", "up5"),
    to_Concate(name='conv10', s_filer=256, n_filer=32+32, offset="(0,0,0)", to="(up5-east)", width=4, height=40, depth=40, caption="concatenate 32+32"),
    to_skip(of='conv0', to='conv10', pos=1.25),
    to_ConvConvRelu(name='conv10_2', s_filer=256, n_filer=(32,32), offset="(0,0,0)", to="(conv10-east)", width=(2,2), height=40, depth=40, caption=" "),


    # *block_Unconv(name="b1", botton="conv5", top='up_b1', s_filer=16, n_filer=256, offset="(2.1,0,0)",
    #               size=(20, 20, 7), opacity=0.5),
    # to_skip(of='ccr_conv4', to='ccr_res_b1', pos=1.25),

    # *block_Unconv(name="b2", botton="up_b1", top='up_b2', s_filer=32, n_filer=256, offset="(2.1,0,0)",
    #               size=(24, 24, 7), opacity=0.5),
    # to_skip(of='ccr_conv3', to='ccr_res_b2', pos=1.25),
    #
    # *block_Unconv(name="b3", botton="up_b2", top='up_b3', s_filer=64, n_filer=128, offset="(2.1,0,0)",
    #               size=(28, 28, 4), opacity=0.5),
    # to_skip(of='ccr_conv2', to='ccr_res_b3', pos=1.25),
    #
    # *block_Unconv(name="b4", botton="up_b3", top='up_b4', s_filer=128, n_filer=64, offset="(2.1,0,0)",
    #               size=(32, 32, 3), opacity=0.5),
    # to_skip(of='ccr_conv1', to='ccr_res_b4', pos=1.25),
    #
    # *block_Unconv(name="b5", botton="up_b4", top='up_b5', s_filer=256, n_filer=32, offset="(2.1,0,0)",
    #               size=(40, 40, 2), opacity=0.5),
    # to_skip(of='conv0', to='ccr_res_b5', pos=1.25),
    #
    to_ConvSoftMax(name="soft1", s_filer=256, offset="(6,6,3)", to="(conv10_2-east)", width=1, height=30, depth=30,
                   caption="softmax"),
    to_connection("conv10_2", "soft1"),

    to_SoftMax2(name="soft2", s_filer=256, offset="(6,-3,3)", to="(conv10_2-east)", width=1, height=30, depth=30,opacity=0.5,
                   caption="motion fields"),
    to_connection("conv10_2", "soft2"),

    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
