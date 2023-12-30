import numpy as np
import plotly.graph_objects as go

import nibabel as nib
import os
import albumentations as alb

import interfaces


def generate_3d_scatter(
    x: np.array, y: np.array, z: np.array, colors: np.array,
    size: int = 3, opacity: float = 0.2, scale: str = 'Teal',
    hover: str = 'skip', name: str = 'MRI'
) -> go.Scatter3d:

    return go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers', hoverinfo=hover,
        marker=dict(
            size=size, opacity=opacity,
            color=colors, colorscale=scale
        ),
        name=name
    )


class ImageReader:

    def __init__(self, root: str, img_size: int = 256, normalize: bool = False, single_class: bool = False):
        pad_size = 256 if img_size > 256 else 224
        self._resize = alb.Compose(
            [
                alb.PadIfNeeded(min_height=pad_size, min_width=pad_size, value=0),
                alb.Resize(img_size, img_size)
            ]
        )
        self._normalize = normalize
        self._single_class = single_class
        self._root = root

    def load_patient_scan(self, idx: int, scan_type: str = 'flair') -> dict:
        patient_id = str(idx).zfill(5)
        scan_filename = f'{self._root}/training/BraTS2021_{patient_id}/BraTS2021_{patient_id}_{scan_type}.nii.gz'

        return self._read_file(idx, scan_type, scan_filename)

    def _read_file(self, idx: int, scan_type: str, path: str) -> dict:
        raw_image = nib.load(path).get_fdata()
        raw_mask = nib.load(path.replace(scan_type, 'seg')).get_fdata()

        processed_frames, processed_masks = [], []

        for frame_idx in range(raw_image.shape[2]):
            frame = raw_image[:, :, frame_idx]
            mask = raw_mask[:, :, frame_idx]
            resized = self._resize(image=frame, mask=mask)
            processed_frames.append(resized['image'])
            processed_masks.append(
                1 * (resized['mask'] > 0) if self._single_class else resized['mask']
            )

        scan_data = np.stack(processed_frames, 0)

        if self._normalize:
            if scan_data.max() > 0:
                scan_data = scan_data / scan_data.max()
            scan_data = scan_data.astype(np.float32)

        return {
            'scan': scan_data,
            'segmentation': np.stack(processed_masks, 0),
            'orig_shape': raw_image.shape
        }


class ImageViewer:

    def __init__(self, reader: ImageReader, mri_downsample: int = 10, mri_colorscale: str = 'Ice'):
        self.reader = reader
        self.mri_downsample = mri_downsample
        self.mri_colorscale = mri_colorscale

    def load_clean_mri(self, image: np.array, orig_dim: int) -> dict:
        shape_offset = image.shape[1] / orig_dim
        z, x, y = (image > 0).nonzero()
        x, y, z = x[::self.mri_downsample], y[::self.mri_downsample], z[::self.mri_downsample]
        colors = image[z, x, y]

        return dict(x=x / shape_offset, y=y / shape_offset, z=z, colors=colors)

    def load_tumor_segmentation(self, image: np.array, orig_dim: int) -> dict:
        tumors = {}
        shape_offset = image.shape[1] / orig_dim
        sampling = {1: 1, 2: 3, 4: 5}

        for class_idx in sampling:
            z, x, y = (image == class_idx).nonzero()
            x, y, z = x[::sampling[class_idx]], y[::sampling[class_idx]], z[::sampling[class_idx]]

            tumors[class_idx] = dict(
                x=x / shape_offset, y=y / shape_offset, z=z,
                colors=class_idx / 4
            )

        return tumors

    def collect_patient_data(self, scan: dict) -> tuple:
        clean_mri = self.load_clean_mri(scan['scan'], scan['orig_shape'][0])
        tumors = self.load_tumor_segmentation(scan['segmentation'], scan['orig_shape'][0])
        markers_created = clean_mri['x'].shape[0] + sum(tumors[class_idx]['x'].shape[0] for class_idx in tumors)

        return [
            generate_3d_scatter(
                **clean_mri, scale=self.mri_colorscale, opacity=0.4,
                hover='skip', name='Brain MRI'
            ),
            generate_3d_scatter(
                **tumors[1], opacity=0.8,
                hover='all', name='Necrotic tumor core'
            ),
            generate_3d_scatter(
                **tumors[2], opacity=0.4,
                hover='all', name='Peritumoral invaded tissue'
            ),
            generate_3d_scatter(
                **tumors[4], opacity=0.4,
                hover='all', name='GD-enhancing tumor'
            ),
        ], markers_created

    def get_3d_scan(self, patient_idx: int, scan_type: str = 'flair') -> go.Figure:
        scan = self.reader.load_patient_scan(patient_idx, scan_type)
        data, num_markers = self.collect_patient_data(scan)

        fig = go.Figure(data=data)
        fig.update_layout(
            title=f'[Patient id:{patient_idx}] brain MRI scan ({num_markers} points)',
            legend_title='Pixel class (click to enable/disable)',
            font=dict(
                family='Courier New, monospace',
                size=14,
            ),
            margin=dict(
                l=0, r=0, b=0, t=50
            ),
            legend=dict(itemsizing='constant')
        )

        return fig


class Downloader(interfaces.Downloader):

    def download(self, url: str, path: str):
        pass
