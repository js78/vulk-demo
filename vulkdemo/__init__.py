import os.path
import numpy as np

from vulk.baseapp import BaseApp
from vulk.vulkanobject import ShaderModule, Pipeline, PipelineShaderStage, \
        PipelineVertexInputState, PipelineViewportState, Viewport, Rect2D, \
        Offset2D, Extent2D, PipelineInputAssemblyState, \
        PipelineRasterizationState, PipelineMultisampleState, \
        PipelineColorBlendAttachmentState, PipelineColorBlendState, \
        AttachmentDescription, SubpassDescription, AttachmentReference, \
        SubpassDependency, Renderpass, CommandPool, Framebuffer, \
        ClearColorValue, Semaphore, SubmitInfo, submit_to_graphic_queue, \
        immediate_buffer, HighPerformanceBuffer, \
        VertexInputBindingDescription, VertexInputAttributeDescription, \
        DescriptorSetLayoutBinding, DescriptorSetLayout, DescriptorPool, \
        DescriptorBufferInfo, WriteDescriptorSet, update_descriptorsets, \
        PipelineLayout, DescriptorPoolSize


class App(BaseApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        w = self.context.width
        h = self.context.height

        # ----------
        # VERTEX BUFFER
        va = [([-0.5, -0.5], [1, 0, 0]),
              ([-0.5, 0.5], [0, 1, 0]),
              ([0.5, 0.5], [0, 0, 1]),
              ([0.5, -0.5], [1, 1, 1])]

        vertices = np.array(va, dtype='2float32, 3uint32')
        vbuffer = HighPerformanceBuffer(self.context, vertices.nbytes,
                                        'vertex')
        with vbuffer.bind(self.context) as b:
            wrapper = np.array(b, copy=False)
            np.copyto(wrapper, vertices.view(dtype=np.uint8), casting='no')

        # ----------
        # INDEX BUFFER
        ia = [0, 1, 2, 0, 2, 3]
        indices = np.array(ia, dtype=np.uint16)
        ibuffer = HighPerformanceBuffer(self.context, indices.nbytes, 'index')
        with ibuffer.bind(self.context) as b:
            wrapper = np.array(b, copy=False)
            np.copyto(wrapper, indices.view(dtype=np.uint8), casting='no')

        # ----------
        # UNIFORM BUFFER
        ua = [1]
        uniforms = np.array(ua, dtype=np.float32)
        ubuffer = HighPerformanceBuffer(self.context, uniforms.nbytes,
                                        'uniform')
        with ubuffer.bind(self.context) as b:
            wrapper = np.array(b, copy=False)
            np.copyto(wrapper, uniforms.view(dtype=np.uint8), casting='no')

        # ----------
        # SHADER MODULES
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'shader')
        with open(os.path.join(path, "vert.spv"), 'rb') as f:
            spirv_vs = f.read()
        with open(os.path.join(path, "frag.spv"), 'rb') as f:
            spirv_fs = f.read()

        vs_module = ShaderModule(self.context, spirv_vs)
        fs_module = ShaderModule(self.context, spirv_fs)

        # ----------
        # FINAL IMAGE LAYOUT
        with immediate_buffer(self.context) as cmd:
            self.context.final_image.update_layout(
                cmd, 'VK_IMAGE_LAYOUT_UNDEFINED',
                'VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL',
                'VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT',
                'VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT',
                0, 'VK_ACCESS_TRANSFER_READ_BIT'
            )

        # ----------
        # RENDERPASS
        attachment = AttachmentDescription(
            self.context.final_image.format, 'VK_SAMPLE_COUNT_1_BIT',
            'VK_ATTACHMENT_LOAD_OP_CLEAR', 'VK_ATTACHMENT_STORE_OP_STORE',
            'VK_ATTACHMENT_LOAD_OP_DONT_CARE',
            'VK_ATTACHMENT_STORE_OP_DONT_CARE',
            'VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL',
            'VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL')
        subpass = SubpassDescription([AttachmentReference(
            0, 'VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL')])
        dependency = SubpassDependency(
            'VK_SUBPASS_EXTERNAL',
            'VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT', 0, 0,
            'VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT',
            'VK_ACCESS_COLOR_ATTACHMENT_READ_BIT | VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT' # noqa
        )
        renderpass = Renderpass(self.context, [attachment], [subpass],
                                [dependency])

        # ----------
        # UBO DESCRIPTOR
        ubo_descriptor = DescriptorSetLayoutBinding(
            0, 'VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER', 1,
            'VK_SHADER_STAGE_FRAGMENT_BIT', None)
        descriptor_layout = DescriptorSetLayout(self.context, [ubo_descriptor])

        pool_size = DescriptorPoolSize('VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER', 1)
        descriptor_pool = DescriptorPool(self.context, [pool_size], 1)
        descriptor_set = descriptor_pool.allocate_descriptorsets(
            self.context, 1, [descriptor_layout])[0]
        descriptorbuffer_info = DescriptorBufferInfo(
            ubuffer.final_buffer, 0, 4)
        descriptor_write = WriteDescriptorSet(
            descriptor_set, 0, 0, 'VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER',
            [descriptorbuffer_info])
        update_descriptorsets(self.context, [descriptor_write], [])

        # ----------
        # PIPELINE
        stages = [PipelineShaderStage(vs_module, 'vertex'),
                  PipelineShaderStage(fs_module, 'fragment')]

        vertex_description = VertexInputBindingDescription(
            0, 20, 'VK_VERTEX_INPUT_RATE_VERTEX')
        position_attribute = VertexInputAttributeDescription(
            0, 0, 'VK_FORMAT_R32G32_SFLOAT', 0)
        color_attribute = VertexInputAttributeDescription(
            1, 0, 'VK_FORMAT_R32G32B32_UINT', 8)
        vertex_input = PipelineVertexInputState([vertex_description],
                                                [position_attribute,
                                                 color_attribute])

        input_assembly = PipelineInputAssemblyState(
            'VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST')

        viewport_state = PipelineViewportState(
            [Viewport(0, 0, w, h, 0, 1)],
            [Rect2D(Offset2D(0, 0), Extent2D(w, h))])

        rasterization = PipelineRasterizationState(
            False, 'VK_POLYGON_MODE_FILL', 1, 'VK_CULL_MODE_BACK_BIT',
            'VK_FRONT_FACE_COUNTER_CLOCKWISE', 0, 0, 0)

        multisample = PipelineMultisampleState(
            False, 'VK_SAMPLE_COUNT_1_BIT', 0)
        depth = None
        blend_attachment = PipelineColorBlendAttachmentState(
            False, 'VK_BLEND_FACTOR_ONE', 'VK_BLEND_FACTOR_ZERO',
            'VK_BLEND_OP_ADD', 'VK_BLEND_FACTOR_ONE', 'VK_BLEND_FACTOR_ZERO',
            'VK_BLEND_OP_ADD', 'VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT | VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT' # noqa
        )
        blend = PipelineColorBlendState(False, 'VK_LOGIC_OP_COPY',
                                        [blend_attachment], [0, 0, 0, 0])
        dynamic = None

        pipeline_layout = PipelineLayout(self.context, [descriptor_layout])

        pipeline = Pipeline(
            self.context, stages, vertex_input, input_assembly,
            viewport_state, rasterization, multisample, depth,
            blend, dynamic, pipeline_layout, renderpass)

        # ----------
        # COMMAND BUFFER
        commandpool = CommandPool(
            self.context, self.context.queue_family_indices['graphic'])
        commandbuffers = commandpool.allocate_buffers(
            self.context, 'VK_COMMAND_BUFFER_LEVEL_PRIMARY', 1)

        framebuffer = Framebuffer(self.context, renderpass,
                                  [self.context.final_image_view], w, h, 1)

        with commandbuffers[0].bind() as cmd:
            # We have to put the good layout because renderpass cannot do it
            # for us, it doesn't know the old layout of the image
            self.context.final_image.update_layout(
                cmd, 'VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL',
                'VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL',
                'VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT',
                'VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT',
                'VK_ACCESS_TRANSFER_READ_BIT',
                'VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT'
            )

            # RenderPass manages the final_image dst layout
            cmd.begin_renderpass(
                renderpass,
                framebuffer,
                Rect2D(Offset2D(0, 0), Extent2D(w, h)),
                [ClearColorValue(float32=[0, 0, 1, 1])]
            )

            cmd.bind_pipeline(pipeline)
            cmd.bind_vertex_buffers(0, 1, [vbuffer.final_buffer], [0])
            cmd.bind_index_buffer(ibuffer.final_buffer, 0,
                                  'VK_INDEX_TYPE_UINT16')
            cmd.bind_descriptor_sets(pipeline_layout, 0, [descriptor_set], [])
            cmd.draw_indexed(6, 0)
            cmd.end_renderpass()

        # ----------
        # SUBMIT
        self.draw_semaphore = Semaphore(self.context)
        self.submit = SubmitInfo([], [], [self.draw_semaphore], commandbuffers) # noqa

    def end(self):
        pass

    def render(self, delta):
        submit_to_graphic_queue(self.context, [self.submit])
        self.context.swap([self.draw_semaphore])
